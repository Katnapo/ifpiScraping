class Constants:
    """
    Constants class containing the scraping dictionary and other constants.

    To Note: An unconventional way to map scraping data. BS4 initially went layer by layer through
    each datapoint, but I took the liberty of placing the "quick_scrape_val" in the layer where the
    desired data would be; this way, the scraper can quickly grab the data without having to go through
    the entire layer structure. However, one benefit of the current structure is useful for testing if the
    site is being updated or if the structure changes.

    """
    scraping_dict = {

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
                    "quick_scrape_val": "one",
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
                    "quick_scrape_val": "one",
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
                        "quick_scrape_val": "many",
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
                                "quick_scrape_val": "many",
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
                    "inner": {
                        "contains": ["class", "text"],
                        "class" : "page-numbers",
                        "special": "many",
                        "quick_scrape_val": "many",
                        "href": None,
                        "text": None,
                        "scrape_target": "text",
                        "type": "a"
                    },
                    }
                }
            }
        }

    # Conventions - When an attribute is not a set value (for example, there is a href but the link varies across
    # elements) include the existence of said attribute in the JSON but set its value to None.

    # URL Home page
    homeUrl = "https://intmusic.net"

    # Database constants
    SQLALCHEMY_DATABASE_URL = "mariadb://root:comsc@localhost:3306/ifpiscraping"
    # Note - structure for connection string is dialect+driver://username:password@host:port/database










