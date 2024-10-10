// API URL + relevant endpoints
const API_URL: string = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'
const childrenEndpoint: string = '/node/children/'
const parentsEndpoint: string = '/node/parents/'
const selectedInfoEndpoint: string = '/node/selected-info/'

/**
 * Fetches the children of a node from the server
 * @param node The node to fetch children for
 * @param includeDeprecated Whether to include deprecated nodes in the response
 * @returns The node with children or null if an error occurred
 * @throws TypeError if a network error occurred
 * @throws Error if any other error occurred (invalid response, invalid node, etc.)
 */
async function fetchChildren(node: any, includeDeprecated: boolean = false): Promise<any> {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  if (!node.has_children) {
    // console.log('Node has no children:', node)
    return null
  }
  try {
    const response = await fetch(
      `${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}?dep=${includeDeprecated}`
    )

    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()

    if (responseData && Array.isArray(responseData.children)) {
      // create a new node object to return
      const newNode = {
        ...node,
        // fetchchildren is only called when the node is expanded so set expanded to true here
        expanded: true,
        children: responseData.children
      }
      // set the expanded flag to false for each child
      newNode.children.forEach((child: any) => {
        child.expanded = false
      })
      return newNode
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

/**
 * Fetches the parents of a node from the server
 * @param node The node to fetch parents for
 * @param includeDeprecated Whether to include deprecated nodes in the response
 * @returns The node with parents or null if an error occurred
 * @throws TypeError if a network error occurred
 * @throws Error if any other error occurred (invalid response, invalid node, etc.)
 */
async function fetchParents(node: any, includeDeprecated: boolean = false): Promise<any> {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  // Only root node, i.e. 'Thing' has no parents
  if (!node.has_parents) {
    // console.log('Node has no parents:', node)
    return null
  }
  try {
    const response = await fetch(
      `${API_URL}${parentsEndpoint}${encodeURIComponent(node.id)}?dep=${includeDeprecated}`
    )

    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()

    if (responseData && Array.isArray(responseData.parents)) {
      // create a new node object to return
      const newNode = {
        ...node,
        // fetchParents is only called when the node is expanded so set expanded to true here
        expanded: true,
        parents: responseData.parents
      }
      // set the expanded flag to false for each parent
      newNode.parents.forEach((parent: any) => {
        parent.expanded = false
      })
      return newNode
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

/**
 * Fetches the selected node's information from the server
 * @param nodeId The ID of the selected node
 * @returns The selected node's information or null if an error occurred
 * @throws TypeError if a network error occurred
 * @throws Error if any other error occurred (invalid response, invalid node, etc.)
 */
async function fetchSelectedInfo(nodeId: string, includeDeprecated: boolean = false): Promise<any> {
  if (!nodeId) {
    console.error('Invalid node ID:', nodeId)
    return null
  }
  try {
    const response = await fetch(
      `${API_URL}${selectedInfoEndpoint}${encodeURIComponent(nodeId)}?dep=${includeDeprecated}`
    )
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
