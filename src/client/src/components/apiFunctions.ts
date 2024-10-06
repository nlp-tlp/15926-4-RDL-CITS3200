// API URL
const API_URL: string = 'http://127.0.0.1:5000'
const childrenEndpoint: string = '/node/children/'
const hierarchyEndpoint: string = '/graph/local-hierarchy/'

// Get children of a node
async function fetchChildren(node: any) {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  if (!node.has_children) {
    console.log('Node has no children:', node)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}`)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()
    if (responseData && Array.isArray(responseData.children)) {
      // create a new node object to return
      const newNode = {
        ...node,
        expanded: true,
        children: responseData.children,
        deprecation: responseData.dep ? responseData.dep : null
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

// Get the local hierarchy of a node
async function getHierarchy(node: any) {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return null
  }
  try {
    const response = await fetch(`${API_URL}${hierarchyEndpoint}${encodeURIComponent(node.id)}`)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return null
    }
    const responseData = await response.json()

    if (responseData.centre_id === node.id) {
      // create a new node object to return
      const newNode = {
        ...node,
        hierarchy: responseData.hierarchy
      }

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

// export the functions
export { fetchChildren, getHierarchy }
