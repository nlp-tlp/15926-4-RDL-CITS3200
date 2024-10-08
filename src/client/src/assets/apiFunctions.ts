// API URL
const API_URL: string = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'
const childrenEndpoint: string = '/node/children/'
const parentsEndpoint: string = '/node/parents/'
const selectedInfoEndpoint: string = '/node/selected-info/'

// Get children of a node
async function fetchChildren(node: any, includeDeprecated: boolean = false): Promise<any> {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  if (!node.has_children) {
    console.log('Node has no children:', node)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}?dep=${includeDeprecated}`)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()
    if (responseData && Array.isArray(responseData.children)) {
      // create a new node object to return
      const newNode = {
        ...node,
        // fetchchildren is only called when the node is expanded so set expanded to true
        expanded: true,
        children: responseData.children,
      }
      // set the expanded flag to false for each child
      newNode.children.forEach((child: any) => {
        child.expanded = false
      })
      return newNode
    } 
    else {
      console.error('Invalid response:', responseData)
      return null
    }
  } catch (error: any) {
    if (error instanceof TypeError) {
      // Network error or other fetch-related error
      console.error('Network error:', error.message)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
    return null
  }
}

// Get parents of a node
async function fetchParents(node: any, includeDeprecated: boolean = false): Promise<any> {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  // Only root node has no parents
  if (!node.has_parents) {
    console.log('Node has no parents:', node)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${parentsEndpoint}${encodeURIComponent(node.id)}?dep=${includeDeprecated}`)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()
    if (responseData && Array.isArray(responseData.parents)) {
      // create a new node object to return
      const newNode = {
        ...node,
        // fetchParents is only called when the node is expanded so set expanded to true
        expanded: true,
        parents: responseData.parents
      }
      // set the expanded flag to false for each parent
      newNode.parents.forEach((parent: any) => {
        parent.expanded = false
      })
      return newNode
    } 
    else {
      console.error('Invalid response:', responseData)
      return null
    }
  } catch (error: any) {
    if (error instanceof TypeError) {
      // Network error or other fetch-related error
      console.error('Network error:', error.message)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
    return null
  }
}


// Get selected node information
async function fetchSelectedInfo(nodeId: any): Promise<any> {
  if (!nodeId) {
    console.error('Invalid node ID:', nodeId)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${selectedInfoEndpoint}${encodeURIComponent(nodeId)}`)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()
    if (responseData) {
      return responseData
    } else {
      console.error('Invalid response:', responseData)
      return null
    }
  } catch (error: any) {
    if (error instanceof TypeError) {
      // Network error or other fetch-related error
      console.error('Network error:', error.message)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
    return null
  }
}




export { fetchChildren, fetchParents, fetchSelectedInfo }