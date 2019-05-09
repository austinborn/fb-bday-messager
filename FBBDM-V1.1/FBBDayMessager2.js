/*
Facebook B-Day Messager 2
Written by Austin Born - 8/5/18

This is my 2nd iteration of the B-Day Messager experiment. This time,
I use the headless Chrome with the Puppeteer library to automate sending 
FB messages without a gui. This allows the task to run quietly in the background.

Notes: Requires node.js and the puppeteer module

To run: node FBBDayMessager2.js USER PASSWORD
*/

const THREE_SECONDS = 3000;

const puppeteer = require('puppeteer');

//Set up log file name
var d = new Date();
var d2 = d.toString().replace(/:/g, '-');
var logName = 'Logs/Log '+d2+".log";

//Configure log4js log system
var log4js = require('log4js');
log4js.configure({
  appenders: {
    console: { type: 'console' },
    fileLogs: { type: 'file', filename: logName }
  },
  categories: {
    default: { appenders: ['console', 'fileLogs'], level: 'trace' }
  }
});
var logger = log4js.getLogger('file');

//Begin Main Execution
(async () => {
  //Launch browser
  logger.trace('Launching browser.');
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();

  //Go to Facebook.com
  logger.trace('Opening Facebook.com.');
  await page.goto('https://www.facebook.com');
  await page.setViewport({ width: 1920, height: 1080});
  
  //Log in
  await page.screenshot({ path: 'File2.png', fullPage: true });
  logger.trace('Logging in.');
  await page.type('#email', process.argv[2]);
  await page.type('#pass', process.argv[3]);
  page.click('[id="loginbutton"]');
  await page.waitForNavigation();
  await page.screenshot({ path: 'File3.png', fullPage: true });

  //Go to Events
  logger.trace('Going to Events.');
  page.click('[id="navItem_2344061033"]');
  await page.waitFor(THREE_SECONDS);
  await page.screenshot({ path: 'File4.png', fullPage: true });

  //Go to Birthdays
  logger.trace('Going to Birthdays.');
  await page.mouse.click(480, 190, { button: 'left' }); //element selector wasn't working :/
  await page.waitFor(THREE_SECONDS);
  await page.screenshot({ path: 'File5.png', fullPage: true });

  //If birthdays today, for each one, write 'Happy birthday!' on their timeline
  if (await page.$('#birthdays_today_card') !== null) {
    await page.screenshot({ path: 'File6.png', fullPage: true });

    //Determine number of bdays
    logger.trace('Determining number of birthdays.');
    var numbdays = (await page.$$('#birthdays_content > div._4-u2._tzh._fbBirthdays__todayCard._4-u8 > div:nth-child(2) > ul > li')).length;

    //Iterate through bdays and send message
    var i;
    for (i = 1; i < numbdays+1; i++){
      await page.click('#birthdays_content > div._4-u2._tzh._fbBirthdays__todayCard._4-u8 > div:nth-child(2) > ul > li:nth-child(x) > div > div._42ef > div > div:nth-child(2) > div > div._6a._5u5j._6b > form'.replace('x', i));
      await page.type('#birthdays_content > div._4-u2._tzh._fbBirthdays__todayCard._4-u8 > div:nth-child(2) > ul > li:nth-child(x) > div > div._42ef > div > div:nth-child(2) > div > div._6a._5u5j._6b > form > input'.replace('x', i), 'Happy birthday!');
      await page.keyboard.press('Enter');
      logger.trace('Sent Happy Birthday #' + i + '.');
    }
  } else {
    logger.trace('No birthdays today.');
  }

  //Close browser
  browser.close();
  logger.trace('Successfully closed browser.');
})()