
class Genealogy:
    """The genealogy and succession order for Envoy of the Kiktil."""

    def __init__(self, originator_name):
        """Constructs an initial genealogy containing no individuals other than
        the Originator.

        Args:
            originator_name: The name of the Originator of the Kiktil species.
        """
        self.originator_name = originator_name
        self.genealogy = {originator_name : []}


    def add_child(self, parent_name, child_name):
        """Adds a new child belonging to a given parent.

        You may assume the parent has previously been added as the child of
        another individual, and that no individual named `child_name` exists.

        Target Complexity: O(1) expected.

        Args:
            parent_name: The name of the parent individual.
            child_name: The name of their new child.
        """
        self.genealogy[parent_name].append(child_name)
        self.genealogy[child_name] = []


    def get_primogeniture_order(self):
        """Returns the primogeniture succession order for Envoy of the Kiktil.

        By primogeniture, succession flows from parent to eldest child, only
        moving to the next youngest sibling after all their elder sibling's
        descendants.

        Target Complexity: O(N), where N is how many indivduals have been added.

        Returns:
            A list of the names of individuals in primogeniture succession order
            starting with the Originator.
        """
        primogeniture_order = []
        queue = [self.originator_name]
    
        while queue:
            parent = queue.pop()  
            primogeniture_order.append(parent) 

            for child in reversed(self.genealogy[parent]):
                queue.append(child)

        return primogeniture_order
    
        
    def get_seniority_order(self):
        """Returns the seniority succession order for Envoy of the Kiktil.

        Seniority order prioritizes proximity to the Originator, only moving on
        to a younger generation after every individual in the previous
        generations. Within a generation, older siblings come before younger,
        and cousins are prioritized by oldest different ancestor.

        Target Complexity: O(N), where N is how many indivduals have been added.

        Returns:
            A list of the names of individuals in seniority succession order
            starting with the Originator.
        """
        seniority_order = []
        queue = [self.originator_name]

        while queue:
            parent = queue.pop(0)
            seniority_order.append(parent)
            queue.extend(self.genealogy[parent])

        return seniority_order
    
        
    def get_cousin_dist(self, lhs_name, rhs_name):
        """Determine the degree and removal of two cousins.

        The order of an individual relative to an ancestor is the number of
        generations separating them. So a child is order 0, a grandchild is
        order 1, and so on.
        Consider the orders of two individuals relative to their most recent
        shared ancestor.
        The degree of the cousin relation of these individuals is the greater of
        their orders.
        The removal of the cousin relation is the difference in their orders.

        Target Complexity: O(N), where N is how many indivduals have been added.

        Args:
            lhs_name: The name of one cousin.
            rhs_name: The name of the other cousin.

        Returns:
            A pair `(degree, removal)` of the degree and removal of the cousin
            relation between the specified individuals.
        """        
        def find_common_ancestor(lhs, rhs):
            lhs_ancestors = []
            
            while lhs != self.originator_name:
                lhs_ancestors.append(lhs)
                lhs = get_parent(lhs)

            while rhs != self.originator_name:
                if rhs in lhs_ancestors:
                    return rhs
                rhs = get_parent(rhs)

            return self.originator_name

        def find_order(name, ancestor):
            order = -1
            while name != ancestor:
                name = get_parent(name)
                order += 1
            return order
        
        def get_parent(name):
            for parent in self.genealogy:
                children = self.genealogy[parent]
                if name in children:
                    return parent
            return None

        common_ancestor = find_common_ancestor(lhs_name, rhs_name)
        lhs_order = find_order(lhs_name, common_ancestor)
        rhs_order = find_order(rhs_name, common_ancestor)

        degree = max(lhs_order, rhs_order)
        removal = abs(lhs_order - rhs_order)
        return (degree, removal)
        