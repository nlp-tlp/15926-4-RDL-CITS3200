import * as d3 from 'd3'

import { fetchChildren } from '@/assets/apiFunctions'

const nodeRadius: number = 7
const nodeDistanceX: number = 25
const nodeDistanceY: number = 350

// draw the children graph
function drawChildrenGraph(data: any, root: any, svg: any, includeDeprecated: boolean) {
  // Construct root node from the data
  root = d3.hierarchy(data)

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // assign x and y properties to the root and its descendants
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Start with the root node expanded
  toggleChildrenCollapse(nodes[0], root, svg, data, includeDeprecated)

  // Render the nodes and links
  renderChildrenNodes(nodes, root, svg, data, includeDeprecated)
  renderChildrenLinks(links, svg)
  renderChildrenExtraLinks(nodes, svg)
}

// update
function updateChildrenGraph(data: any, root: any, svg: any, includeDeprecated: boolean) {
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.children : null))

  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  const nodes = root.descendants()
  const links = root.links()

  renderChildrenNodes(nodes, root, svg, data, includeDeprecated)
  renderChildrenLinks(links, svg)
  renderChildrenExtraLinks(nodes, svg)
}

// render the nodes of the graph - uses nodes array
function renderChildrenNodes(
  nodes: any,
  root: any,
  svg: any,
  childrenHierarchyData: any,
  includeDeprecated: boolean
) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node-children').data(nodes, (d: any) => d.data.id)
  // console.log('Nodes:', nodes)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node-children')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      event.stopPropagation()
      toggleChildrenCollapse(d, root, svg, childrenHierarchyData, includeDeprecated)
    })

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    // set the fill color based on the presence of children
    // .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
    .attr('fill', (d: any) => {
      if (d.data.dep) {
        return '#fc1455'
      } else {
        // if is root node
        if (d.data.id === childrenHierarchyData.id) {
          return '#FFCF00'
        }
        return d.data.has_children ? '#69b3a2' : '#999'
      }
    })
    // set the cursor style based on the presence of children
    .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
    .attr('stroke', '#444')
    .attr('stroke-width', (d: any) => (d.data.has_children ? 2 : 0))

  // append text to the node
  nodeEnter
    .append('text')
    .attr('dy', '.35em')
    // set the text position based on the expanded state - left if expanded, right if collapsed
    // .attr('x', (d: any) => (d.data.expanded ? -15 : 10))
    // .style('text-anchor', (d: any) => (d.data.expanded ? 'end' : 'start'))
    .text((d: any) => d.data.label)

  // merge the enter and update selections
  const nodeUpdate = nodeEnter.merge(nodeSelection)

  // Update the node positions and visibility
  nodeUpdate
    .attr('transform', (d: any) => `translate(${d.y},${d.x})`)
    .style('display', (d: any) => (d.parent && !d.parent.data.expanded ? 'none' : null))

  // Update the text position based on the expanded state
  nodeUpdate
    .select('text')

    // x: root at 0 and children otherwise based on expanded state
    .attr('x', (d: any, i: number) => (i === 0 ? 0 : d.data.expanded ? -15 : 10))
    // y: root at -20 and children not changed
    .attr('y', (d: any, i: number) => (i === 0 ? -20 : 0))
    // text-anchor: root at middle and children based on expanded state
    .style('text-anchor', (d: any, i: number) =>
      i === 0 ? 'middle' : d.data.expanded ? 'end' : 'start'
    )
    .style('font-weight', (d: any) => (d.data.dep ? 300 : 450))
    .style('font-style', (d: any) => (d.data.dep ? 'italic' : 'normal'))

  // remove the nodes that are no longer needed
  nodeSelection.exit().remove()
}

// toggle the collapse/expansion of a node
async function toggleChildrenCollapse(
  node: any,
  root: any,
  svg: any,
  childrenHierarchyData: any,
  includeDeprecated: boolean
) {
  console.log('depr', includeDeprecated)

  if (!node.data.has_children) {
    console.log('Node has no children:', node.data.label)
    return
  }

  if (!node.data.children) {
    // Fetch the children of the node
    const newNodeData = await fetchChildren(node.data, includeDeprecated)
    updateChildrenHierarchyData(node, newNodeData, childrenHierarchyData)
  } else {
    // if root node, do not collapse
    if (node.data.id === childrenHierarchyData.id) {
      return
    }
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }

  updateChildrenGraph(childrenHierarchyData, root, svg, includeDeprecated)
}

// find the node in childrenHierarchyData and update it
function updateChildrenHierarchyData(node: any, newNodeData: any, childrenHierarchyData: any) {
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      currentNode.children = newNodeData.children.map((child: any) => ({
        ...child,
        expanded: false,
        children: null
      }))
      currentNode.expanded = true
      return true
    }

    if (currentNode.children) {
      for (const child of currentNode.children) {
        if (updateNode(child)) {
          return true
        }
      }
    }

    return false
  }

  updateNode(childrenHierarchyData)
}

// render the extra links of the graph
function renderChildrenExtraLinks(nodes: any, svg: any) {
  // Create an array to store the extra links
  const extraLinks: any = []
  // Iterate over the nodes to find the extra links
  nodes.forEach((d: any) => {
    if (d.data.extra_parents) {
      d.data.extra_parents.forEach((parent: any) => {
        const parentNode = nodes.find((node: any) => node.data.id === parent.id)
        if (parentNode) {
          extraLinks.push({ source: parentNode, target: d })
        }
      })
    }
  })

  // Select all extra links and bind the data
  const extraLink: any = svg
    .selectAll('path.extra-link-children')
    .data(extraLinks, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const extraLinkEnter = extraLink
    .enter()
    .insert('path', 'g')
    .attr('class', 'extra-link-children')
    .attr('stroke', 'red')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow-extra)')
    .attr('stroke-dasharray', '5,5')

  // merge the enter and update selections
  const extraLinkUpdate = extraLinkEnter.merge(extraLink)

  // update the extra link positions to use the diagonal function
  extraLinkUpdate.attr('d', (d: any) => customDiagonal(d, 13))

  // remove the extra links that are no longer needed
  extraLink.exit().remove()
}

// render the links of the graph
function renderChildrenLinks(links: any, svg: any) {
  // Select all links and bind the data
  const link = svg.selectAll('path.link-children').data(links, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const linkEnter = link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link-children')
    .attr('stroke', '#999')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')

  // merge the enter and update selections
  const linkUpdate = linkEnter.merge(link)

  // update the link positions
  linkUpdate.attr('d', (d: any) => customDiagonal(d, 13))

  // remove the links that are no longer needed
  link.exit().remove()
}

/**
 * Create a diagonal path generator.
 */
function customDiagonal(d: any, offset = 13) {
  const sourceX = d.source.y
  const sourceY = d.source.x
  const targetX = d.target.y
  const targetY = d.target.x

  // Determine if it's a forward or backward link
  const isForward = targetX > sourceX

  // Check if the link is vertical or near-vertical
  if (Math.abs(sourceX - targetX) < 1) {
    // For vertical links, adjust the end point slightly to make arrow visible
    const arrowAdjustment = isForward ? -offset : offset
    return `
      M ${sourceX},${sourceY}
      L ${targetX},${targetY + arrowAdjustment}
    `
  }

  // For non-vertical links, apply offset and use a curved path
  const adjustedTargetX = isForward ? targetX - offset : targetX + offset
  const midX = (sourceX + adjustedTargetX) / 2
  return `
    M ${sourceX},${sourceY}
    C ${midX},${sourceY} ${midX},${targetY} ${adjustedTargetX},${targetY}
  `
}

export { drawChildrenGraph }
