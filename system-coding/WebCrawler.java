import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * 多线程网页爬虫，单文件完整实现
 * 限制：最多抓取1000个唯一页面
 */
public class WebCrawler {
    // 配置参数
    private static final int MAX_CRAWL_COUNT = 1000;
    private static final int THREAD_POOL_SIZE = 8; // 工作线程数量

    // 共享资源：待爬取URL队列（临界资源）
    private final BlockingQueue<String> workQueue;
    // 共享资源：已访问URL集合，去重（临界资源）
    private final Set<String> visitedUrls;
    // 当前已经抓取成功的页面数量
    private int crawledCount;
    // 线程池
    private final ExecutorService threadPool;
    // 标记爬虫是否应该停止
    private final AtomicBoolean isShutdown;

    public WebCrawler() {
        workQueue = new LinkedBlockingQueue<>();
        visitedUrls = new HashSet<>();
        crawledCount = 0;
        threadPool = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        isShutdown = new AtomicBoolean(false);
    }

    /**
     * 爬虫入口
     * @param seedUrl 种子URL
     */
    public void startCrawl(String seedUrl) {
        // 初始化种子URL，临界区操作
        synchronized (visitedUrls) {
            if (!visitedUrls.contains(seedUrl) && crawledCount < MAX_CRAWL_COUNT) {
                visitedUrls.add(seedUrl);
                workQueue.offer(seedUrl);
            }
        }

        // 提交持续运行的工作线程
        for (int i = 0; i < THREAD_POOL_SIZE; i++) {
            threadPool.submit(this::workerLoop);
        }
    }

    /**
     * 工作线程主循环：持续从队列获取URL执行爬取
     */
    private void workerLoop() {
        try {
            while (!isShutdown.get()) {
                String currentUrl = workQueue.poll(500, TimeUnit.MILLISECONDS);
                if (currentUrl == null) {
                    // 队列轮询超时，检查是否可以终止
                    checkTermination();
                    continue;
                }

                // ========== 网络IO + 页面解析【不在临界区内！重点！】==========
                List<String> discoveredUrls = crawlPage(currentUrl);

                // ========== 只有操作共享集合时进入临界区 ==========
                synchronized (visitedUrls) {
                    crawledCount++;
                    if (crawledCount >= MAX_CRAWL_COUNT) {
                        isShutdown.set(true);
                        continue;
                    }
                    // 将新发现URL入队（去重校验）
                    for (String newUrl : discoveredUrls) {
                        if (!visitedUrls.contains(newUrl)) {
                            visitedUrls.add(newUrl);
                            workQueue.offer(newUrl);
                        }
                    }
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * 模拟：访问页面，耗时IO操作，返回页面内所有链接
     * 真实实现：HTTP GET 请求 + Jsoup解析HTML提取<a href>
     */
    private List<String> crawlPage(String url) throws InterruptedException {
        System.out.printf("线程[%s] 正在爬取页面: %s%n", Thread.currentThread().getName(), url);
        // 模拟网络延迟 10~100ms
        Thread.sleep(new Random().nextInt(90) + 10);

        // 模拟从页面提取若干子链接
        List<String> links = new ArrayList<>();
        Random random = new Random();
        int linkNum = random.nextInt(5);
        for (int i = 0; i < linkNum; i++) {
            links.add(url + "/sub-" + random.nextInt(10000));
        }
        return links;
    }

    /**
     * 终止条件判断：队列为空，不再有新任务，则关闭爬虫
     */
    private void checkTermination() {
        synchronized (visitedUrls) {
            if (workQueue.isEmpty() || crawledCount >= MAX_CRAWL_COUNT) {
                isShutdown.set(true);
            }
        }
    }

    /**
     * 优雅释放资源
     */
    public void shutdown() {
        isShutdown.set(true);
        threadPool.shutdown();
        try {
            if (!threadPool.awaitTermination(2, TimeUnit.SECONDS)) {
                threadPool.shutdownNow();
            }
        } catch (InterruptedException e) {
            threadPool.shutdownNow();
        }
        System.out.println("爬虫结束，总共抓取页面数量：" + crawledCount);
    }

    public static void main(String[] args) {
        WebCrawler crawler = new WebCrawler();
        crawler.startCrawl("https://seed-example.com");

        // 主线程等待一段时间，实际生产由终止条件自动退出
        try {
            TimeUnit.SECONDS.sleep(15);
        } catch (InterruptedException ignored) {}
        crawler.shutdown();
    }
}