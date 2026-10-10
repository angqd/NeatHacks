# Task families (review)

Check each family: does every question below belong? Mark a task in the wrong family by id. `*` = selected in the draft 60.


## finance_analysis (10)
Stock, crypto, commodity and personal-finance analysis and reports.

-   `88ccea26` [multi_capability] Analyze Apple's stock for the past year and summarize it in a PPT in /root/ppt/apple.pptx.
-   `37d72d03` [multi_capability] Analyze the last 24h of BTC and remind me if there is anything I need to pay special attention to
- * `ef7126b3` [multi_capability] I need a daily financial brief. Fetch today's economic news, cross-reference it with relevant stock movements, and then generate a
-   `b276e772` [multi_capability] I have 9.5g gold, please estimate its value based on the current price of gold
- * `470f7ac1` [multi_capability] How are Samsung Electronics and SK Hynix doing today? I need their current stock prices, the daily percentage change for each, and
- * `b6281fad` [taxonomy_collision] I have 18.9g silver, please estimate its value based on the current price
- * `41899b5b` [semantic_distance]  I'm considering doing some initial research on a potential investment in the Korean market. Could you help me gather comprehensiv
-   `80bb6782` [multi_capability] My after-tax income last month was 15,000 CNY, and my main expenses were 3,000 CNY for rent, 2,500 CNY for meals, 500 CNY for tran
-   `39c4c9fc` [near_duplicate] Tell me the price of nvidia's stock right now.
- * `38c156c5` [multi_capability] Help me do a full investment analysis on Nvidia's stock

## news_and_trends (9)
Current news, trending topics and sentiment across news and social platforms.

- * `0180954e` [taxonomy_collision] Show me today's trending topics in the gaming world across all platforms.
- * `8aaa7e7f` [taxonomy_collision] Find today's top LLM-related news.
- * `e28e8dcb` [ambiguity] Help me view recent finance-related news, categorize financial news by sentiment, and extract key entities (companies, people, pro
- * `c4d6c051` [ambiguity] Based on the current Fear & Greed Index and recent news, do you think it's a good time to take the plunge?
- * `ab11def3` [near_duplicate] Any recent negative news about Bitcoin? Also, tell me how the Crypto Fear & Greed Index has changed over the past three days.
- * `cf6ea2ca` [near_duplicate] Tell me what's the big news in AI today.
-   `84326f9f` [near_duplicate] Read the comments on hacker news story 44490510 and help me summarize the views in the comments.
- * `d1ea5598` [none] Get today's bbc news, reserved for finance related content.
-   `614189f6` [multi_capability] What's on the zhihu and bilibili trendings today? Help me recommend something tech related!

## geo_location (8)
Geocoding, routing, nearby places, commute/neighborhood analysis and weather by location.

-   `dda8ea55` [multi_capability] I'm planning a trip to the Forbidden City in Beijing, show me where to park and what's interesting to do within 1km distance?
-   `5a2720cd` [multi_capability] There are three of us. One person is in Haidian Huangzhuang, another is at Chaoyang Joy City, and the third is at Shijingshan Hosp
- * `afd60e13` [multi_capability] I'm driving an EV with a 300km range from Beijing to Chengdu. Can you map out a route with all the charging stations I'll need?
- * `04282571` [multi_capability] Plan a bike route from UCAS Zhongguancun Campus to UCAS Yanqihu Campus, including an estimated travel time.
- * `8f26fc1a` [taxonomy_collision] My office is located at Jin Mao Tower, 88 Century Avenue, Pudong New Area, Shanghai.
I'm looking at a potential apartment in the N
- * `b84fbf2e` [taxonomy_collision] I'm considering relocating to New York City and need a comprehensive understanding of a potential neighborhood's livability. Pleas
-   `1f6a6db5` [multi_capability] I plan to go to Shinjuku Gyoen from Tokyo Tower and then find a highly rated Japanese restaurant nearby for lunch. Give me restaur
-   `cab818f4` [near_duplicate] What's the weather like in Beijing in the last few days? Give me some advice on what to wear!

## web_research_writing (8)
Fetch or search the web/Wikipedia/open data and write up findings to a file.

-   `f2a9eb67` [semantic_distance] Generate a deep report of bitcoin and save it in /root/markdown/bitcoin.md
-   `9fc8b7f3` [semantic_distance] Help me find Mr. Lu Yaojie's resume in the Chinese Information Processing Laboratory of the Institute of Software and save it to /
-   `7180c69a` [taxonomy_collision] Make a web page about the history of AI based on Wikipedia saved at /root/html/ai.html.
-   `4d7582c4` [multi_capability] Download New York's Air Quality report from Government Data, saved at /root/csv/NY_AIR_QUALITY.csv
-   `83da9f72` [multi_capability] Analyze the visual marketing strategy from the iPhone 16 page at https://www.apple.com/iphone-16/ and save the summary as a Markdo
-   `9bc7feb8` [multi_capability] Provide a foundational overview of Convolutional Neural Networks (CNNs), referencing Wikipedia. Generate a simple CNN example as a
- * `665e1166` [multi_capability] Read the Wikipedia article on Llullaillaco, which briefly describes the content of this article, saved to /root/markdown/Llullaill
- * `4cbd9682` [multi_capability] I am writing a popular science article on ‘Causes of the Fall of the Roman Empire’. Please help me to list at least three main cau

## document_authoring (8)
Create Word, PowerPoint, PDF or Markdown documents from gathered content.

- * `0e3287cb` [multi_capability] Generate a well-formatted PDF report titled wechat_reading_report.pdf in /root/pdf, summarizing current WeChat Reading trends and 
-   `230fb273` [multi_capability] Find today's LeetCode Daily Challenge and generate a detailed markdown document in /root/markdown/leetcode_daily.md that provides 
-   `56d7fbdb` [multi_capability] Find the trending GitHub repositories. For the top one, read its Deepwiki. Then, draft a Markdown intro document for it in /root/m
- * `a984d31b` [multi_capability] Help me make a STEINS;GATE introduction PPT and help me save it to /root/ppt/STEINS_GATE.pptx.
-   `e023dd0e` [multi_capability] Generate a presentation on the latest Apple product information. Save it to /root/ppt/apple_news.pptx.
- * `fbe982c3` [multi_capability] I need a Word document summarizing NIO. Please title it 'NIO Company Overview' and include three headed sections: a brief introduc
-   `17a4aef0` [multi_capability] Generate a well-formatted PDF report  in /root/pdf/douban_report.pdf, summarizing current douban trends.
-   `423f89ba` [multi_capability] Help me create an example word that needs to have headings, tables, body, footnotes and insert clock.png under /root/picture and s

## academic_search (7)
Find, read and compare research papers, clinical trials and biomedical literature.

- * `e9df60b1` [near_duplicate] Please help me find the latest articles about 'MCP' on arXiv. Identify the potentially most influential papers among them and anal
- * `6b7fc66e` [taxonomy_collision] Generate a research summary for NCT04280705 and save it as Markdown to /root/markdown/NCT04280705.md.
- * `7bda47e8` [near_duplicate] Introduce me to the article on arxiv 2203.12277
- * `2bf318d4` [multi_capability] What are the emerging treatment strategies for head and neck cancer, write the report to /root/markdown/cancer.md?
- * `fa451c3f` [near_duplicate] Read the paper in /root/pdf/WebArena.pdf, and find the latest papers in this area
- * `4aa079dd` [multi_capability] Read the paper webarena, mind2web and mind2web2, then create a Comparison Report in /root/markdown/compare_webagent.md
-   `5c19a347` [multi_capability] Find the latest research paper in the web agents. Identify the best one, read the full text, and then tell me its main motivation,

## local_files (7)
Read, list, diff and query local files and spreadsheets.

- * `d116bda4` [semantic_distance] Read the data under /root/excel/people_data.xlsx and tell me Sophia Moore's bmi.
-   `9a18862e` [near_duplicate] Get line 10 of /root/txt/Android.txt, please note that this file is very large
- * `1ef11556` [near_duplicate] Read all the articles in the /root/pdf/embodied_ai_papers directory. Compare their similarities and differences, then write a repo
- * `086e2393` [none] Read the file /root/word/exchange.docx, tell me who did not give a gift
- * `507f592a` [none] Read the customer information in /root/csv/customers-100.csv and tell me Sheryl Meyers's email address
-   `31086c2d` [near_duplicate] What files are in my /root/music folder?
- * `2e190c2a` [taxonomy_collision] What are the changes in my log files /root/txt/log_today.txt and /root/txt/log_yesterday.txt, help me to find out all the differen

## shopping_research (6)
Product recommendations, price lookup and deals, often via browsing.

-   `08644b1a` [semantic_distance] Help me recommend any cheap goodies worth buying recently? Save this information to /root/excel/goods.xlsx.
-   `3819a831` [multi_capability] Find the latest standard iphone prices at amazon.
-   `6265fd4a` [semantic_distance] Help me recommend some consumer electronics that are worth buying these days.
- * `2f8db365` [semantic_distance] Recommend a gaming PC build for playing the latest Call of Duty, along with an approximate budget.
-   `ea6e95fa` [multi_capability] Help me find the top 5 best selling gpus from amazon and tell me the links directly.
- * `15aa8d9b` [semantic_distance] I want to buy a 34-inch curved monitor, please help me recommend some items with prices and links to buy.

## developer_tools (6)
Coding aids: library docs, UI components, package versions, git.

-   `567c79c3` [multi_capability] Help me write a quick start tutorial for Ant Design in markdown at /root/markdown/antd_tutorial.md.
-   `ec6f4fe5` [multi_capability] Create a Next.js middleware that checks for a valid JWT in cookies and redirects unauthenticated users to `/login` in /root/code/m
- * `de75630e` [semantic_distance]  I'm looking at a PR and need to know if these libs are outdated. com.fasterxml.jackson.core:jackson-databind:2.13.4, org.apache.p
-   `cf1fca1e` [multi_capability] Analyze and compare echarts-for-react, react-chartjs-2, and Tremor. It's for a FinTech app, so my top priorities are a deep securi
- * `a93169d7` [multi_capability] Tell me about the repository details in the /root/git directory
-   `90098a9c` [semantic_distance] I'm using shadcn/ui to build a 'create post' page. I have two input fields, one for the title and one for the content. I want the 

## media_visual_audio (6)
Audio analysis, image decoding, diagrams, drawing, charts and video transcripts.

-   `99d7541a` [multi_capability] Please perform a comprehensive analysis of the audio file located at /root/music/mixkit-retro-game-emergency-alarm-1000.wav. The a
-   `4de2e9f7` [near_duplicate] Read the sales data under /root/excel/Local_Electronic_Sales.xlsx, plot it as a bar chart by month and save it in /root/figs/sale.
-   `91cce869` [semantic_distance] Draw a flowchart of a fast sorting algorithm using Mermaid.
-   `cda14e48` [multi_capability] draw cowboy using canvas 
-   `1a3ffa81` [multi_capability] Extract the key points of this TED talk in https://www.youtube.com/watch?v=arj7oStGLkU, organize them into a mind map, and tell me
- * `3a5cfe49` [near_duplicate] What does this base64 image mean?
iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAN1wAADdcBQiibeAAA

## lifestyle_utilities (6)
Recipes, calendar, fortune, art lookup and small utilities.

- * `0b21b741` [none] What are the 八字 of a boy born on August 8, 2008 at 11:00 am?
- * `e8f13600` [near_duplicate] There are three people eating in the house this week, I'm allergic to shrimp and my son doesn't eat scallions, so please help me r
-   `3c65e618` [semantic_distance] Recommend me a combination of dishes for a potluck dinner for three people and then tell me what ingredients I need to prepare in 
- * `00e13e2e` [semantic_distance] find the painting "Corridor in the Asylum" and give me some background information,
- * `49cdaab7` [taxonomy_collision] We have organized an online raffle with the following list of participants: [‘Alice’, ‘Bob’, ‘Charlie’, ‘David’, ‘Eve’]. Please ch
-   `ffd5f6fb` [semantic_distance] I need you to pull up the Chinese almanac and find me the best dates to get married in the near future. Give me a list of the most

## travel_planning (5)
Multi-day trips, train tickets, accommodation and itineraries.

-   `be3f2275` [multi_capability] Help me check the high-speed train tickets from Beijing to Shanghai on next Wednesday.
-   `10b5dbf7` [multi_capability] Help me arrange a three-day trip from Beijing to Tianjin tomorrow, round-trip by rail, give me a detailed timetable and include an
- * `f2b074b5` [semantic_distance] Help me find homestays in Paris, France, I want to stay tomorrow, about 3 days, one adult.
- * `2293b5eb` [multi_capability] Give me a two-day tour of Beijing based on the recent weather, and my hotel is in the Haidian District
- * `0dafdf66` [near_duplicate] Find the earliest available high-speed train from Beijing South to Shanghai South for tomorrow. What's the departure time and tick

## gaming (4)
Game statistics, character builds and card lookup.

- * `629106a5` [semantic_distance] My goal is to reach Radiant in Valorant, what should I focus on to improve and start climbing?
- * `5b2087e4` [taxonomy_collision] I play mid lane in League of Legends and want to improve. Provide champion recommendations with optimal item builds, runes, and su
- * `fab605cf` [taxonomy_collision] What is the current effect text of 'Sky Striker Ace = Zero', and what are its ATK and DEF? Show me the picture.
-   `29fa007d` [semantic_distance] I just pulled Jiyan and want to build a team around him as my main DPS. Can you recommend a good starter team for me? I need a sub

## file_conversion (3)
Convert or transform file formats (docx to pdf, markdown to mindmap, bib to Word).

-   `860f7b99` [multi_capability] Get deepwiki for vercel/ai and convert its structure to mindmap
- * `71a7a42a` [multi_capability] Convert the reference list in /root/txt/paper_list.bib into a Word document. Please use APA formatting and save the final file at 
-   `b050f277` [multi_capability] Convert /root/word/CV.docx and /root/word/Report_Card.docx to PDF, merge the two resulting files, and save the final combined docu

## security_network (2)
Domain reconnaissance and site trust checks.

-   `2b96c022` [multi_capability] Run a full reconnaissance on www.baidu.com. Give me a markdown report on /root/markdown/baidu_report.md with whois information and
-   `36d95b6f` [semantic_distance] I received an email from amaz0n.com asking me to click on a link to enter my account information. Is this site official for Amazon
