class Page(object):
    """
    page object
    
    parameters
    ----------
    name : str
        page name
        
    pagerank : float, optional
        initial pagerank score to be updated through iteration. it
        is usually set to 1/N, where N equals number of pages.
    
    attributes
    ----------
    parents : list
        represents inbound links
    children : list
        represents outbound links
    """
    def __init__(self, name, pagerank=1.0):
        self.name = name
        self.pagerank = pagerank
        self.parents = []
        self.children = []
        
    def add_parent(self, page_obj):
        self.parents.append(page_obj)
        
    def add_child(self, page_obj):
        self.children.append(page_obj)
        
    def count(self):
        return len(self.children)
    
    def update_pagerank(self, pagerank):
        self.pagerank = pagerank