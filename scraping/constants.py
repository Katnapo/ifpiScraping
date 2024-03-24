class Constants:

    # Scraping constants
    scrapingDict = {

        "SongPage":{
            "TitleData":{
                "contains": ["class"],
                "class": "entry-title",
                "type": "div",
                "inner": {
                    "contains": ["class", "text"],
                    "text": None,
                    "scrape_target": "text",
                    "class": "fleft",
                    "type": "h2"
                }
            },

            "DateData":{
                "contains": ["class"],
                "class": "entry-meta",
                "type": "div",
                "inner": {
                    "contains": ["style", "text"],
                    "style": "float:right;",
                    "text": None,
                    "type": "span",
                    "scrape_target": "text"
                }
            },

            "DownloadLinkData":{
                "contains": ["class"],
                "class": "entry-content",
                "type": "div",
                "inner": {
                    "contains": ["class"],
                    "class": "edldv",
                    "type": "div",
                    "inner": {
                        "contains": ["href", "target", "rel", "text"],
                        "type": "a",
                        "target": "_blank",
                        "rel": "nofollow",
                        "href": None,
                        "text": "Download",
                        "special": "many",
                        "scrape_target": "href"
                    }
                }
            }

        },

        "HomePage" :{
            "SongListData":{
                "contains": ["id"],
                "id": "content",
                "type": "div",
                "inner": {
                    "contains": ["class"],
                    "class": "entry",
                    "type": "div",
                    "id" : "post-",
                    "special": "many",
                    "inner": {
                        "contains": ["class"],
                        "type": "div",
                        "class": "entry-meta",
                        # Note - potential to also grab href link by title here if needed, diverge from path here
                        "inner": {
                            "contains": ["class"],
                            "class": "readmore",
                            "type": "span",
                            "inner": {
                                "contains": ["href", "rel", "text"],
                                "type": "a",
                                "href": None,
                                "rel": "bookmark",
                                "scrape_target": "href",
                                "text": "Read More"
                            }
                        }
                    }
                }
            },
            "PageNavigationData":{
                "contains": ["id"],
                "id": "content",
                "type": "div",
                "inner": {
                    "contains": ["class"],
                    "class": "pagination",
                    "type": "div",
                    "special": "top",
                    "inner": {
                        "contains": ["class", "text"],
                        "class" : "page-numbers",
                        "special": "many",
                        "href": None,
                        "text": None,
                        "scrape_target": "text",
                        "type": "a"
                    },
                    }
                }
            }
        }

    # URL Home page
    homeUrl = "https://intmusic.net"












