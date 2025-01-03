// API URL + relevant endpoints
const API_URL: string = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'
const childrenEndpoint: string = '/node/children/'
const parentsEndpoint: string = '/node/parents/'
const selectedInfoEndpoint: string = '/node/selected-info/'
const infoEndpoint: string = '/node/info/'
const searchEndpoint: string = '/search/'
const searchLimit: number = 25

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
    if (!responseData || !Array.isArray(responseData.children)) {
      console.error('Invalid response:', responseData)
      return null
    }

    const newNode = {
      ...node,
      expanded: true,
      children: responseData.children
    }

    newNode.children.forEach((child: any) => {
      child.expanded = false
    })
    return newNode
  } catch (error: any) {
    console.error('Error:', error.message)
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
    if (!responseData || !Array.isArray(responseData.parents)) {
      console.error('Invalid response:', responseData)
      return null
    }

    const newNode = {
      ...node,
      expanded: true,
      parents: responseData.parents
    }

    newNode.parents.forEach((parent: any) => {
      parent.expanded = false
    })
    return newNode
  } catch (error: any) {
    console.error('Error:', error.message)
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
    if (!responseData) {
      console.error('Invalid response:', responseData)
      return null
    }

    return responseData
  } catch (error: any) {
    console.error('Error:', error.message)
    return null
  }
}

/**
 * Fetches the node's information from the server
 * @param nodeId The ID of the node
 * @returns The node's information or null if an error occurred
 * @throws TypeError if a network error occurred
 * @throws Error if any other error occurred (invalid response, invalid node, etc.)
 */
async function fetchNodeInfo(nodeId: string) {
  if (!nodeId) {
    console.error('Invalid node ID:', nodeId)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${infoEndpoint}${encodeURIComponent(nodeId)}`)
    if (!response.ok) {
      console.error('Failed to fetch node info:', response.status)
      return null
    }
    const responseData = await response.json()
    if (!responseData) {
      console.error('Invalid response:', responseData)
      return null
    }

    const nodeInfoDisplay = {
      id: '',
      label: '',
      definition: '',
      deprecation: '',
      parents: [] as string[],
      types: [] as string[]
    }
    nodeInfoDisplay.id = responseData.id
    nodeInfoDisplay.label = responseData.label
    nodeInfoDisplay.definition = responseData.definition
    nodeInfoDisplay.deprecation = responseData.dep ? responseData.dep.slice(0, -1) : ''

    nodeInfoDisplay.parents = responseData.parents
    nodeInfoDisplay.types = responseData.types

    return nodeInfoDisplay
  } catch (error: any) {
    console.error('Error:', error.message)
    return null
  }
}

/**
 * Fetches search results from the server
 * @param query The search query
 * @param searchOption The search option ('id' or 'rdf')
 * @param includeDeprecated Whether to include deprecated nodes in the response
 * @returns An object with the search results and an error message (if any)
 */
async function search(
  query: string,
  searchOption: string,
  includeDeprecated: boolean = false
): Promise<any> {
  const results: any[] = []
  let errorMessage = ''

  try {
    const endpoint = searchOption === 'id' ? `${searchEndpoint}id/` : `${searchEndpoint}label/`
    const response = await fetch(
      `${API_URL}${endpoint}${encodeURIComponent(query)}?limit=${searchLimit}&dep=${includeDeprecated}`
    )
    const data = await response.json()

    if (data.results && data.results.length > 0) {
      data.results.forEach((result: any) => {
        results.push({
          id: result.id,
          label: result.label,
          dep: result.dep
        })
      })
    } else {
      errorMessage = 'No results found.'
    }
  } catch (error: any) {
    console.error('Error fetching search results:', error)
    errorMessage = 'Failed to fetch search results. Please try again later.'
  }

  return { results, errorMessage }
}

export { fetchChildren, fetchNodeInfo, fetchParents, fetchSelectedInfo, search }
