import os
import shutil
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from content import SITE_CONFIG, CATEGORIES, ARTICLES, PAGES

OUT_DIR = ".."

def format_date_rfc822(dt_str):
    from email.utils import formatdate
    import time
    dt = datetime.strptime(dt_str, "%Y-%m-%d")
    return formatdate(time.mktime(dt.timetuple()))

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def load_template(name):
    with open(f"templates/{name}", "r", encoding="utf-8") as f:
        return f.read()

def build_schemas(page_type, data):
    schemas = []
    
    # Organization Schema
    schemas.append({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_CONFIG["site_name"],
        "url": SITE_CONFIG["site_url"],
        "logo": f"{SITE_CONFIG['site_url']}/assets/icon-512.png"
    })

    # WebSite Schema
    schemas.append({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_CONFIG["site_name"],
        "url": SITE_CONFIG["site_url"],
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_CONFIG['site_url']}/search.html?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    })
    
    if page_type == "article":
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": data["title"],
            "description": data["description"],
            "image": f"{SITE_CONFIG['site_url']}/assets/icon-512.png",
            "author": {
                "@type": "Person",
                "name": SITE_CONFIG["author_name"],
                "url": f"{SITE_CONFIG['site_url']}/about.html"
            },
            "publisher": {
                "@type": "Organization",
                "name": SITE_CONFIG["site_name"],
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{SITE_CONFIG['site_url']}/assets/icon-512.png"
                }
            },
            "datePublished": data["publish_date"],
            "dateModified": data["publish_date"],
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_CONFIG['site_url']}/{data['category']}/{data['slug']}.html"
            }
        })
        
        # Breadcrumb List
        schemas.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_CONFIG["site_url"]},
                {"@type": "ListItem", "position": 2, "name": CATEGORIES[data["category"]]["title"], "item": f"{SITE_CONFIG['site_url']}/{data['category']}/index.html"},
                {"@type": "ListItem", "position": 3, "name": data["title"], "item": f"{SITE_CONFIG['site_url']}/{data['category']}/{data['slug']}.html"}
            ]
        })
        
        # FAQPage schema
        schemas.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"Is {data['keyword']} covered by the VA?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Coverage depends on whether your condition is deemed service-connected or if you meet specific income thresholds. Always check with your local VA eligibility office."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How long does the process take?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "From initial appointment to receiving care or devices, it can take anywhere from a few weeks to several months."
                    }
                }
            ]
        })

    return json.dumps(schemas)

def generate():
    # Copy assets from src/assets to ../assets
    if os.path.exists("assets"):
        if not os.path.exists(os.path.join(OUT_DIR, "assets")):
            os.makedirs(os.path.join(OUT_DIR, "assets"), exist_ok=True)
        import distutils.dir_util
        distutils.dir_util.copy_tree("assets", os.path.join(OUT_DIR, "assets"))
        
    base_tpl = load_template("base.html")
    article_tpl = load_template("article.html")
    page_tpl = load_template("page.html")
    index_tpl = load_template("index.html")
    category_tpl = load_template("category.html")
    search_tpl = load_template("search.html")

    sitemap_urls = []
    sitemap_urls.append({"loc": SITE_CONFIG["site_url"] + "/", "priority": "1.0"})

    # Create Categories Navigation
    nav_html = '<ul>'
    nav_html += '<li><a href="/">Home</a></li>'
    for k, v in CATEGORIES.items():
        nav_html += f'<li><a href="/{k}/index.html">{v["title"]}</a></li>'
    nav_html += '<li><a href="/about.html">About Us</a></li>'
    nav_html += '</ul>'
    
    # Generate Index (Home)
    latest_articles_html = ""
    for art in reversed(ARTICLES[-6:]):
        url = f"/{art['category']}/{art['slug']}.html"
        latest_articles_html += f'<article class="card"><h3><a href="{url}">{art["title"]}</a></h3><p>{art["description"]}</p></article>'
    
    index_content = index_tpl.replace("{{latest_articles}}", latest_articles_html)
    
    final_index = base_tpl.replace("{{content}}", index_content)
    final_index = final_index.replace("{{title}}", f"{SITE_CONFIG['site_name']} | VA Benefits & Hearing Guides")
    final_index = final_index.replace("{{description}}", SITE_CONFIG["description"])
    final_index = final_index.replace("{{nav}}", nav_html)
    final_index = final_index.replace("{{schemas}}", build_schemas("website", {}))
    final_index = final_index.replace("{{site_name}}", SITE_CONFIG["site_name"])
    final_index = final_index.replace("{{canonical_url}}", f"{SITE_CONFIG['site_url']}/")
    final_index = final_index.replace("{{author_name}}", SITE_CONFIG["author_name"])
    
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(final_index)
        
    # Generate Search Page
    final_search = base_tpl.replace("{{content}}", search_tpl)
    final_search = final_search.replace("{{title}}", f"Search | {SITE_CONFIG['site_name']}")
    final_search = final_search.replace("{{description}}", "Search our database of articles on veterans hearing aids.")
    final_search = final_search.replace("{{nav}}", nav_html)
    final_search = final_search.replace("{{schemas}}", "")
    final_search = final_search.replace("{{site_name}}", SITE_CONFIG["site_name"])
    final_search = final_search.replace("{{canonical_url}}", f"{SITE_CONFIG['site_url']}/search.html")
    final_search = final_search.replace("{{author_name}}", SITE_CONFIG["author_name"])

    with open(os.path.join(OUT_DIR, "search.html"), "w", encoding="utf-8") as f:
        f.write(final_search)

    # Generate Standard Pages
    for slug, data in PAGES.items():
        page_html = page_tpl.replace("{{title}}", data["title"])
        body = data["body"].replace("{{author_name}}", SITE_CONFIG["author_name"])
        body = body.replace("{{author_bio}}", SITE_CONFIG["author_bio"])
        page_html = page_html.replace("{{body}}", body)
        
        final_page = base_tpl.replace("{{content}}", page_html)
        final_page = final_page.replace("{{title}}", f"{data['title']} | {SITE_CONFIG['site_name']}")
        final_page = final_page.replace("{{description}}", data["description"])
        final_page = final_page.replace("{{nav}}", nav_html)
        final_page = final_page.replace("{{schemas}}", "")
        final_page = final_page.replace("{{site_name}}", SITE_CONFIG["site_name"])
        url_path = f"/{slug}.html" if slug != "404" else "/404.html"
        final_page = final_page.replace("{{canonical_url}}", f"{SITE_CONFIG['site_url']}{url_path}")
        final_page = final_page.replace("{{author_name}}", SITE_CONFIG["author_name"])
        
        with open(os.path.join(OUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(final_page)
            
        if slug != "404":
            sitemap_urls.append({"loc": f"{SITE_CONFIG['site_url']}/{slug}.html", "priority": "0.8"})

    # Organize articles by category
    category_articles = {k: [] for k in CATEGORIES}
    search_index = []
    
    # Generate Articles
    for art in ARTICLES:
        category_articles[art["category"]].append(art)
        cat_title = CATEGORIES[art["category"]]["title"]
        url_path = f"/{art['category']}/{art['slug']}.html"
        full_url = f"{SITE_CONFIG['site_url']}{url_path}"
        
        search_index.append({
            "title": art["title"],
            "url": url_path,
            "description": art["description"],
            "content": f"{art['title']} {art['keyword']} {cat_title}"
        })
        
        # Related articles (just pick 3 from same category, excluding self)
        related_html = ""
        related_count = 0
        for rel in ARTICLES:
            if rel["category"] == art["category"] and rel["slug"] != art["slug"]:
                rel_url = f"/{rel['category']}/{rel['slug']}.html"
                related_html += f'<li><a href="{rel_url}">{rel["title"]}</a></li>'
                related_count += 1
                if related_count >= 3:
                    break
        
        art_html = article_tpl.replace("{{title}}", art["title"])
        art_html = art_html.replace("{{body}}", art["body"])
        art_html = art_html.replace("{{category_title}}", cat_title)
        art_html = art_html.replace("{{category_url}}", f"/{art['category']}/index.html")
        art_html = art_html.replace("{{publish_date}}", art["publish_date"])
        art_html = art_html.replace("{{author_name}}", SITE_CONFIG["author_name"])
        art_html = art_html.replace("{{author_bio}}", SITE_CONFIG["author_bio"])
        art_html = art_html.replace("{{related_articles}}", related_html)
        art_html = art_html.replace("{{current_url}}", full_url)
        art_html = art_html.replace("{{url_encoded_title}}", art["title"].replace(" ", "%20"))
        
        final_art = base_tpl.replace("{{content}}", art_html)
        final_art = final_art.replace("{{title}}", f"{art['title']} | {SITE_CONFIG['site_name']}")
        final_art = final_art.replace("{{description}}", art["description"])
        final_art = final_art.replace("{{nav}}", nav_html)
        final_art = final_art.replace("{{schemas}}", build_schemas("article", art))
        final_art = final_art.replace("{{site_name}}", SITE_CONFIG["site_name"])
        final_art = final_art.replace("{{canonical_url}}", full_url)
        final_art = final_art.replace("{{author_name}}", SITE_CONFIG["author_name"])
        
        out_path = os.path.join(OUT_DIR, art["category"], f"{art['slug']}.html")
        ensure_dir(out_path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_art)
            
        sitemap_urls.append({"loc": full_url, "priority": "0.9"})
        
    # Generate Category Hubs
    for cat_slug, cat_data in CATEGORIES.items():
        hub_articles = ""
        for art in category_articles[cat_slug]:
            url = f"/{art['category']}/{art['slug']}.html"
            hub_articles += f'<article class="card"><h3><a href="{url}">{art["title"]}</a></h3><p>{art["description"]}</p></article>'
            
        cat_html = category_tpl.replace("{{title}}", cat_data["title"])
        cat_html = cat_html.replace("{{description}}", cat_data["description"])
        cat_html = cat_html.replace("{{articles}}", hub_articles)
        
        full_url = f"{SITE_CONFIG['site_url']}/{cat_slug}/index.html"
        
        final_cat = base_tpl.replace("{{content}}", cat_html)
        final_cat = final_cat.replace("{{title}}", f"{cat_data['title']} | {SITE_CONFIG['site_name']}")
        final_cat = final_cat.replace("{{description}}", cat_data["description"])
        final_cat = final_cat.replace("{{nav}}", nav_html)
        final_cat = final_cat.replace("{{schemas}}", "")
        final_cat = final_cat.replace("{{site_name}}", SITE_CONFIG["site_name"])
        final_cat = final_cat.replace("{{canonical_url}}", full_url)
        final_cat = final_cat.replace("{{author_name}}", SITE_CONFIG["author_name"])
        
        out_path = os.path.join(OUT_DIR, cat_slug, "index.html")
        ensure_dir(out_path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_cat)
            
        sitemap_urls.append({"loc": full_url, "priority": "0.8"})

    # Write Search Index
    search_js = f"window.searchIndex = {json.dumps(search_index)};"
    with open(os.path.join(OUT_DIR, "assets", "searchIndex.js"), "w", encoding="utf-8") as f:
        f.write(search_js)

    # Generate Sitemap
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for s_url in sitemap_urls:
        url_el = ET.SubElement(root, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = s_url["loc"]
        pri_el = ET.SubElement(url_el, "priority")
        pri_el.text = s_url["priority"]
        lastmod = ET.SubElement(url_el, "lastmod")
        lastmod.text = datetime.now().strftime("%Y-%m-%d")
        
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(os.path.join(OUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xmlstr)
        
    # Generate RSS
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    t = ET.SubElement(channel, "title")
    t.text = SITE_CONFIG["site_name"]
    l = ET.SubElement(channel, "link")
    l.text = SITE_CONFIG["site_url"]
    d = ET.SubElement(channel, "description")
    d.text = SITE_CONFIG["description"]
    
    for art in reversed(ARTICLES[-20:]):
        item = ET.SubElement(channel, "item")
        it = ET.SubElement(item, "title")
        it.text = art["title"]
        il = ET.SubElement(item, "link")
        il.text = f"{SITE_CONFIG['site_url']}/{art['category']}/{art['slug']}.html"
        idesc = ET.SubElement(item, "description")
        idesc.text = art["description"]
        ipub = ET.SubElement(item, "pubDate")
        ipub.text = format_date_rfc822(art["publish_date"])
        
    rssstr = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    with open(os.path.join(OUT_DIR, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rssstr)
        
    # Generate robots.txt
    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE_CONFIG['site_url']}/sitemap.xml\n"
    with open(os.path.join(OUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print("Site built successfully in out/")

if __name__ == "__main__":
    generate()
