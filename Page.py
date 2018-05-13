class Page(object):
    """
    page object. in pagerank, this is the equivalent of a website.
    
    parameters
    ----------
    name : str
        page name
        
    pagerank : float, optional
        initial pagerank score to be updated through iteration. it
        is usually set to 1/N, where N equals number of pages.
    
    attributes
    ----------
    parents : list of Page objects
        represents inbound links. a parent is a Page object that
        points to this Page object.
    children : list of Page objects
        represents outbound links.
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

class PageRank(object):
    def __init__(self):
        self.ls_nodes = []
    
    def add_page(self, node):
        self.ls_nodes.append(node)
        
    def calculate(self, n_iterations, d):
        n = float(len(self.ls_nodes))

        for _ in range(n_iterations):

            # for each page...
            for page in self.ls_nodes:

                # update its pagerank by inspecting its children's pagerank
                updated_prob = (1-d) * 1/n

                for parent in page.parents:

                    # parents with high pageranks but few outbound are best
                    updated_prob += d * (parent.pagerank)/parent.count()
                page.update_pagerank(updated_prob)