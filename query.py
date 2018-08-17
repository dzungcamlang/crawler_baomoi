def search_to_file(term):
    es = Elasticsearch([{'host': '206.189.92.171', 'port': 9200}])
    # Initialize the scroll
    page = es.search(
        request_timeout=30,
        index='ospg_post_*',
        doc_type='post',
        scroll='2m',
        size=5000,
        body={
            "query": {
                "bool": {
                    "filter": [
                        {
                            "query_string": {
                                "fields": [
                                    "message",
                                    "content"
                                ],
                                "query": "\"{}\"".format(term)
                            }
                        },
                        {
                            "query_string": {
                                "fields": [
                                    "docType"
                                ],
                                "query": "user_post"
                            }
                        }
                    ],
                    "must_not": [],
                    "should": [],
                    "minimum_should_match": 0
                }
            }
        })

    sid = page['_scroll_id']
    hits = page['hits']['hits']
    result = []
    for post in hits:
        result.append(post['source']['userid'] + '' + post['_source']['docId'])
        print(post['source']['userid'] + '' + post['_source']['docId'])
        print(len(result))
    scroll_size = page['hits']['total']  # Start scrolling
    while scroll_size > 0:
        print('scroll size', scroll_size)
        print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        hits = page['hits']['hits']
        for post in hits:
            result.append(post['source']['userid'] +
                          '' + post['_source']['docId'])
            print(post['source']['userid'] + '' + post['_source']['docId'])
            print(len(result))
    # Do something with the obtained page
    file_io.write_new_file('data/post_id/' + term.replace(' ', '_'), result)
