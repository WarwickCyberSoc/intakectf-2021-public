import { createClient } from "redis";
import puppeteer from "puppeteer";

const browserOptions = {
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-background-networking",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-gpu",
    "--disable-sync",
    "--disable-translate",
    "--hide-scrollbars",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
  ],
  executablePath: "google-chrome-stable",
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

(async () => {
  const client = createClient({
    url: "redis://localhost:6379",
  });

  client.on("error", (err) => console.log("Redis Client Error", err));

  await client.connect();

  while (true) {
    // Retrieve all the draft stories
    const storyIds = await client.keys("draft_*");

    for (const storyId of storyIds) {
      const browser = await puppeteer.launch(browserOptions);
      const page = await browser.newPage();

      console.log("Viewing story", storyId);
      await page.goto(`http://127.0.0.1/post.php?id=${storyId}`, {
        waitUntil: "networkidle2",
        timeout: 15000,
      });

      await browser.close();

      await client.del(storyId);

      await sleep(2500);
    }

    console.log("Sleeping for 10 seconds...");
    await sleep(10000);
  }
})();
