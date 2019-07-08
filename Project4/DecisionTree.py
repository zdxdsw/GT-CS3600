from math import log
import sys
class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. 
  islead (boolean): whether this is a leaf. False.
  """
  
  def __init__(self,attr):
    self.children = {} # key: attribute value, value: child_node
    self.attr = attr
    self.isleaf = False

class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.
    
    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """
    def __init__(self,value):
        self.value = value
        self.isleaf = True
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print str(self)
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.isleaf:
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.isleaf:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)
  
  def classify(self, classificationData):
    """
    Uses the classification tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with this tree.
    """
    #YOUR CODE HERE
    cur = self.root
    while(not cur.isleaf):
      a = cur.attr
      for c in cur.children:
        if classificationData[a] == c:
          cur = cur.children[c]
          break
    return cur.value
  
def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE
    for e in examples:
      if e[attrName] == attrValue:
        newExamples.append(e)
    return newExamples
  
def getClassCounts(examples,className):
    """
    Helper function to get a dictionary of counts of different class values
    in a set of examples. That is, this returns a dictionary where each key 
    in the list corresponds to a possible value of the class and the value
    at that key corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """
    classCounts = {}
    #YOUR CODE HERE
    for e in examples:
      if e[className] in classCounts:
        classCounts[e[className]] += 1
      else:
        classCounts[e[className]] = 1
    return classCounts

def getMostCommonClass(examples,className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples,className)
    return max(counts, key=counts.get) if len(examples)>0 else None

def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a dictionary of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
	  That is, this returns a dictionary of dictionaries, where each key  
	  corresponds to a possible value of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for the attribute
        className (str): the name of the class
    Returns:
        dictionary<str,dictionary<str,int>>
        This is a dictionary that for each value of the attribute has a
        dictionary from class values to class counts, as in getClassCounts
    """
    attributeCounts={}
    #YOUR CODE HERE
    for v in attrValues:
      dic = {}
      for e in examples:
        if e[attrName] == v:
          if e[className] in dic:
            dic[e[className]] += 1
          else:
            dic[e[className]] = 1
      attributeCounts[v] = dic
    return attributeCounts
        

def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE
    total = 0
    for c in classCounts:
      total += c
    en = 0
    for c in classCounts:
      p = float(c)/float(total)
      en += p * log(p,2)
    return -en
   

def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    classCounts = getClassCounts(examples,className)
    total_points = 0
    for k in classCounts:
      total_points += classCounts[k]
    result = 0
    for v in attrValues:
      scope = getPertinentExamples(examples, attrName, v)
      classcount = getClassCounts(scope, className)
      subset = 0
      en_arg = []
      for k in classcount:
        subset += classcount[k]
        en_arg.append(classcount[k])
      result += (float(subset)/float(total_points))*setEntropy(en_arg)
    return result
    
          
def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    r = remainder(examples,attrName,attrValues,className)
    classCounts = getClassCounts(examples, className)
    en_arg = []
    for k in classCounts:
      en_arg.append(classCounts[k])
    en = setEntropy(en_arg)
    return en-r
  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE
    total = 0
    for c in classCounts:
      total += c
    result = 0
    for c in classCounts:
      p = float(c)/float(total)
      result -= p*p
    return 1+ result
  
def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE
    classCounts = getClassCounts(examples, className)
    total = 0.0
    for k in classCounts:
      total += classCounts[k]
    result = 0
    for v in attrValues:
      per_e = getPertinentExamples(examples, attrName, v)
      classcount = getClassCounts(per_e, className)
      l = []
      subset = 0.0
      for k in classcount:
        subset += classcount[k]
        l.append(classcount[k])
      gini = giniIndex(l)
      result += (float(subset)/float(total))*gini
    if result == 0:
      return sys.maxint
    return 1.0/result
    
def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
                          If there is no examples in the node
        setScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
                              accept a list of classCounts
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
                              arg: (examples,attrName,attrValues,className)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE
    if len(examples) == 0:
      root = LeafNode(defaultLabel)
      return root
    if len(examples) == 1:
      label = examples[0][className]
      root = LeafNode(label)
      return root
    first_label = examples[0][className]
    same = True
    # all points have the same label ###############
    # no need to further split
    for e in examples:
      if not e[className] == first_label:
        same = False
        break
    if same:
      root = LeafNode(first_label)
      return root
    ################################################
    # run out of attributes: also make a leaf
    if len(remainingAttributes) == 0:
      most_label = getMostCommonClass(examples, className)
      root = LeafNode(most_label)
      return root
    ################################################
    # Choose the optimal attribute according to splitting criterion
    max_score = -float('inf')
    optimal_a = None
    for a in remainingAttributes:
      score = gainFunc(examples,a,attributeValues[a],className)
      if score>max_score:
        optimal_a = a
        max_score = score
    #print("choose attribute: ",optimal_a)
    root = Node(optimal_a)
    child_attr = []
    for r in remainingAttributes:
      if not r==optimal_a:
        child_attr.append(r)
    def_label = getMostCommonClass(examples, className)
    # recursively make child trees according to each value of the optimal attribute
    dic = {}
    for v in attributeValues[optimal_a]:
      per_e = getPertinentExamples(examples, optimal_a, v)
      dic[v] = makeSubtrees(child_attr,per_e,attributeValues,className,def_label,setScoreFunc,gainFunc)
    root.children = dic
    return root
      
    
def makePrunedTree(examples, attrValues,className,setScoreFunc,gainFunc,q):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makePrunedSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc,q))
    
def makePrunedSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc,q):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE (Extra Credit)
    if len(examples) == 0:
      leaf = LeafNode(defaultLabel)
      return leaf
    if len(examples) == 1:
      label = examples[0][className]
      root = LeafNode(label)
      return root
    first_label = examples[0][className]
    same = True
    # all points have the same label ###############
    # no need to further split
    for e in examples:
      if not e[className] == first_label:
        same = False
        break
    if same:
      root = LeafNode(first_label)
      return root
    ############################################################
    # run out of attributes: also make a leaf
    if len(remainingAttributes) == 0:
      most_label = getMostCommonClass(examples, className)
      root = LeafNode(most_label)
      return root
    ############################################################
    # Choose the optimal attribute according to splitting criterion
    max_score = -float('inf')
    optimal_a = None
    for a in remainingAttributes:
      score = gainFunc(examples,a,attributeValues[a],className)
      if score>max_score:
        optimal_a = a
        max_score = score
    # print("choose attribute: ",optimal_a)
    
    # chi-square check #########################################
    attr_count = getAttributeCounts(examples, optimal_a, attributeValues[optimal_a], className)
    # a dictionary, key is a value of the attribute,
    # value is another dictionary:{class, classcount} for all points with optimal_a = key
    dic = {} # How many points have optimal_a = v
    for e in examples:
      v = e[optimal_a]
      if v in dic:
        dic[v] += 1
      else:
        dic[v] = 1

    classCounts = getClassCounts(examples, className) # How many points have label = c
    chi_2 = 0
    for v in attr_count:
      for c in attr_count[v]:
        o = float(attr_count[v][c]) # How many points have optimal_a = v && label = c; observed count
        e = float(classCounts[c]*dic[v])/float(len(examples)) # expected count
        chi_2 += (o-e)*(o-e)/e
    df = len(attributeValues[optimal_a]) - 1 # degree of freedom
    
    # prune, do not split anymore ##############################
    from scipy.stats import chi2
    prob = chi2.cdf(chi_2, df)
    if 1- prob > q:
      label = getMostCommonClass(examples, className)
      leaf = LeafNode(label)
      return leaf
    
    # continue split, the same as makeSubTrees() ###############
    root = Node(optimal_a)
    child_attr = []
    for r in remainingAttributes:
      if not r==optimal_a:
        child_attr.append(r)
    def_label = getMostCommonClass(examples, className)
    # recursively make child trees according to each value of the optimal attribute
    dic = {}
    for v in attributeValues[optimal_a]:
      per_e = getPertinentExamples(examples, optimal_a, v)
      dic[v] = makePrunedSubtrees(child_attr,per_e,attributeValues,className,def_label,setScoreFunc,gainFunc,q)
    root.children = dic
    return root
