import * as d3 from 'd3'

import { fetchParents } from '@/assets/apiFunctions'

// node dimensions + spacing
const nodeRadius: number = 7
const nodeDistanceX: number = 30
const nodeDistanceY: number = 370

// node visuals
const nodeDeprecatedColor: string = '#FC1455'
const nodeNormalColor: string = 'lightsteelblue'
const nodeHoverColor: string = '#AAA1F6'
const textHoverColor: string = '#6C63FF'
const nodeRootColor: string = '#FFCF00'
const nodeNoParentsColor: string = '#999'

/**
 * Draw the parents hierarchy graph.
 * @param data The data to be displayed in the graph
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to draw the graph on
 * @param props The properties of the graph
 * @param emit The emit function to emit events to the parent component
 */
function drawParentsGraph(data: any, root: any, svg: any, props: any, emit: any) {
  if (!data) {
    return
  }
  // Construct the hierarchy
  root = d3.hierarchy(data)

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // Generate the tree layout - assigns x and y positions to all nodes
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Expand the root node to start with 1 level of parents
  toggleParentsCollapse(nodes[0], root, svg, data, props, emit)

  // Render the nodes, links and extra links
  renderParentsNodes(nodes, root, svg, data, props, emit)
  renderParentsLinks(links, svg)
  renderExtraChildrenLinks(nodes, svg)
}

/**
 * Update the parents hierarchy graph.
 * @param data The data to be displayed in the graph
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to draw the graph on
 * @param props The properties of the graph
 * @param emit The emit function to emit events to the parent component
 */
function updateParentsGraph(data: any, root: any, svg: any, props: any, emit: any) {
  // Construct the hierarchy - use the parents property to determine the parent-child relationship
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.parents : null))

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // Generate the tree layout - assigns x and y positions to all nodes
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Render the nodes, links and extra links
  renderParentsNodes(nodes, root, svg, data, props, emit)
  renderParentsLinks(links, svg)
  renderExtraChildrenLinks(nodes, svg)
}

/**
 * Render the nodes of the graph.
 * @param nodes The nodes to be rendered
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to draw the graph on
 * @param parentHierarchyData The data of the parent hierarchy
 * @param props The properties of the graph
 * @param emit The emit function to emit events to the parent component
 */
function renderParentsNodes(
  nodes: any,
  root: any,
  svg: any,
  parentHierarchyData: any,
  props: any,
  emit: any
) {
  // Select all nodes and bind the data using the node id
  const nodeSelection = svg.selectAll('g.node-parents').data(nodes, (d: any) => d.data.id)

  // on enter, append a group element and set the class
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node-parents')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      // Prevent the click event from propagating to the parent elements
      event.stopPropagation()
      toggleParentsCollapse(d, root, svg, parentHierarchyData, props, emit)
    })

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    .attr('fill', (d: any) => {
      if (d.data.dep) {
        return nodeDeprecatedColor
      } else {
        // if it is root node
        if (d.data.id === parentHierarchyData.id) {
          return nodeRootColor
        }
        return d.data.has_parents ? nodeNormalColor : nodeNoParentsColor
      }
    })
    // set the cursor style based on the presence of parents, if root, leave default
    .attr('cursor', (d: any, i: number) =>
      i === 0 ? 'default' : d.data.has_parents ? 'pointer' : 'default'
    )
    .attr('stroke', '#444')
    .attr('stroke-width', (d: any) => (d.data.has_parents ? 2 : 0))

  // append text to the node
  nodeEnter
    .append('text')
    .attr('dy', '.35em')
    .text((d: any) => d.data.label)

  // merge the enter and update selections
  const nodeUpdate = nodeEnter.merge(nodeSelection)

  // node update
  nodeUpdate
    // Invert both x and y coordinates to rotate the tree
    .attr('transform', (d: any) => `translate(${-d.y},${-d.x})`)
    // in case something went wrong with toggling the collapse, hide the children
    .style('display', (d: any) => (d.parent && !d.parent.data.expanded ? 'none' : null))

  // Update the text
  nodeUpdate
    .select('text')
    // display none if prop showLabels is false
    .style('display', props.showLabels ? 'block' : 'none')
    // x: root at 0 and parents otherwise based on expanded state
    .attr('x', (d: any, i: number) => (i === 0 ? 0 : d.data.expanded ? -10 : 15))
    // y: root at -20 and parents not changed
    .attr('y', (d: any, i: number) => (i === 0 ? -20 : 0))
    // text-anchor: root at middle and parents based on expanded state
    .style('text-anchor', (d: any, i: number) =>
      i === 0 ? 'middle' : d.data.expanded ? 'end' : 'start'
    )
    .style('font-weight', (d: any) => (d.data.dep ? 325 : 450))
    .style('font-style', (d: any) => (d.data.dep ? 'italic' : 'normal'))

  // label hover effect
  nodeUpdate
    .select('text')
    .style('cursor', () => 'pointer')
    .on('mouseover', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement)
        .style('fill', textHoverColor)
        .style('font-weight', (d: any) => (d.data.dep ? 450 : 700))
    })
    .on('mouseout', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement)
        .style('fill', '')
        .style('font-weight', (d: any) => (d.data.dep ? 325 : 450))
    })
    .on('click', (event: any, d: any) => {
      event.stopPropagation()
      emit('label-clicked', d.data.id)
    })

  // node circle hover effect
  nodeUpdate
    .select('circle')
    .on('mouseover', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGCircleElement).style('fill', (d: any) => {
        if (d.data.dep) {
          return nodeDeprecatedColor
        } else {
          if (d.data.id === parentHierarchyData.id) {
            return nodeRootColor
          }
          return nodeHoverColor
        }
      })
    })
    .on('mouseout', (event: MouseEvent) =>
      d3.select(event.currentTarget as SVGCircleElement).style('fill', (d: any) => {
        if (d.data.dep) {
          return nodeDeprecatedColor
        } else {
          if (d.data.id === parentHierarchyData.id) {
            return nodeRootColor
          }
          return d.data.has_parents ? nodeNormalColor : nodeNoParentsColor
        }
      })
    )

  // remove the nodes that are no longer needed
  nodeSelection.exit().remove()
}

/**
 * Toggle the collapse of the parents of a node.
 * @param node The node to toggle the collapse for
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to draw the graph on
 * @param parentHierarchyData The data of the parent hierarchy
 * @param props The properties of the graph
 * @param emit The emit function to emit events to the parent component
 */
async function toggleParentsCollapse(
  node: any,
  root: any,
  svg: any,
  parentHierarchyData: any,
  props: any,
  emit: any
) {
  if (!node.data.has_parents) {
    // console.log('Node has no parents:', node.data.label)
    return
  }

  if (!node.data.parents) {
    // Fetch the parents of the node
    const newNodeData = await fetchParents(node.data, props.includeDeprecated)
    updateParentsHierarchyData(node, newNodeData, parentHierarchyData)
  } else {
    // if it is the root node, do not collapse
    if (node.data.id === parentHierarchyData.id) {
      return
    }
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }
  // Call the update function to re-render the graph with the new data
  updateParentsGraph(parentHierarchyData, root, svg, props, emit)
}

/**
 * Update the parents hierarchy data.
 * @param node The node to update the parents for
 * @param newNodeData The new data of the node
 * @param parentHierarchyData The data of the parent hierarchy
 */
function updateParentsHierarchyData(node: any, newNodeData: any, parentHierarchyData: any) {
  if (!newNodeData) {
    return
  }
  // Update the parents of the node in the parent hierarchy data
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      currentNode.parents = newNodeData.parents.map((parent: any) => ({
        ...parent,
        expanded: false,
        parents: null
      }))
      currentNode.expanded = true
      return true
    }

    if (currentNode.parents) {
      for (const parent of currentNode.parents) {
        if (updateNode(parent)) {
          return true
        }
      }
    }
    return false
  }
  updateNode(parentHierarchyData)
}

/**
 * Render the extra children (in parents hierarchy graph) links of the graph.
 * @param nodes The nodes of the graph
 * @param svg The SVG element to draw the graph on
 */
function renderExtraChildrenLinks(nodes: any, svg: any) {
  // Create an array to store the extra links
  const extraLinks: any = []

  // Iterate over the nodes to find the extra links
  nodes.forEach((d: any) => {
    if (d.data.extra_children) {
      d.data.extra_children.forEach((children: any) => {
        const childrenNode = nodes.find((node: any) => node.data.id === children.id)
        if (childrenNode) {
          extraLinks.push({ target: childrenNode, source: d })
        }
      })
    }
  })

  // Select all extra links and bind the data
  const extraLink: any = svg
    .selectAll('path.extra-link-parents')
    .data(extraLinks, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const extraLinkEnter = extraLink
    .enter()
    .insert('path', 'g')
    .attr('class', 'extra-link-parents')
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

/**
 * Render the parents links of the graph.
 * @param links The links to be rendered
 * @param svg The SVG element to draw the graph on
 */
function renderParentsLinks(links: any, svg: any) {
  // Select all links and bind the data
  const link = svg.selectAll('path.link-parents').data(links, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const linkEnter = link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link-parents')
    .attr('stroke', '#999')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')

  // merge the enter and update selections
  const linkUpdate = linkEnter.merge(link)

  // update the link positions using the diagonal function
  linkUpdate.attr('d', (d: any) => customDiagonal(d, 13))

  // remove the links that are no longer needed
  link.exit().remove()
}

/**
 * Custom diagonal function for the links.
 * @param d The link data
 * @param offset The offset of the link (default is 13)
 */
function customDiagonal(d: any, offset = 13) {
  // Swap the x and y coordinates since the parents hierarchy is rotated
  const sourceX = -d.source.y
  const sourceY = -d.source.x
  const targetX = -d.target.y
  const targetY = -d.target.x

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

export { drawParentsGraph }
