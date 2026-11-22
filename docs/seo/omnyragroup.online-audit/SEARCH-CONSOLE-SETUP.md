# Google Search Console setup (about 10 minutes)

Search Console is Google's free dashboard. It shows which searches your site appears for, how many people click, and which pages Google has or has not indexed. Do this after the `fix/seo-critical` changes are live.

## 1. Add the site
1. Go to https://search.google.com/search-console and sign in with the Google account that should own the site (for example omnyra.training@gmail.com).
2. Click **Add property** and choose **Domain** (the left box, not "URL prefix").
3. Type `omnyragroup.online` and click **Continue**. Google shows a TXT record starting with `google-site-verification=`. Copy it.

## 2. Prove you own the domain
1. Log in to the company where you bought omnyragroup.online (GoDaddy, Hostinger, Namecheap, etc.) and open its **DNS settings**.
2. Add a new record: Type **TXT**, Name/Host **@**, Value = the text you copied, TTL default.
3. Save, go back to Search Console and click **Verify**. If it fails, wait 15 to 60 minutes and try again; DNS can be slow.
4. Do not delete this TXT record later; Search Console re-checks it.

## 3. Submit the sitemap
1. In Search Console, open **Sitemaps** in the left menu.
2. Enter `sitemap.xml` and click **Submit**. Status should change to "Success" within a day.

## 4. Ask Google to index the key pages
1. Paste `https://omnyragroup.online/` into the search bar at the top and press Enter.
2. Click **Request indexing**. Repeat for `/programs/` and `/resources/`. (There is a daily limit of roughly 10 requests.)

## 5. Check back after 3 to 7 days
- **Pages** report: shows indexed vs not indexed pages and the reason for each. Exam Portal pages should move to "Excluded by noindex tag".
- **Performance** report: shows search queries, impressions, clicks and average position. Export it (top right, Export, Google Sheets or CSV) and share it for the next round of SEO work.

## Also worth doing (5 minutes each)
- **Bing Webmaster Tools** (https://www.bing.com/webmasters): sign in and choose **Import from Google Search Console**. Bing also powers ChatGPT search and DuckDuckGo.
- **Google Business Profile** (https://business.google.com): create a profile as an online service business ("GRC training"), no address shown, and link the website. Ask real students to leave reviews there.
