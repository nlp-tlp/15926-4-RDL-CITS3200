import * as d3 from 'd3'

import { fetchChildren } from '@/assets/apiFunctions'

// node dimensions + spacing
const nodeRadius: number = 7
const nodeDistanceX: number = 30
const nodeDistanceY: number = 370

// node visuals
const nodeDeprecatedColor: string = '#FC1455'
const nodeNormalColor: string = '#69B3A2'
const nodeHoverColor: string = '#16F1A2'
const textHoverColor: string = '#19C1A2'
const nodeRootColor: string = '#FFCF00'
const nodeNoParentsColor: string = '#999'

/**
 * Draw the children graph
 * @param data The data to draw the graph with
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to draw the graph on
 * @param props The props of the component
 * @param emit The emit function of the component
 */
function drawChildrenGraph(data: any, root: any, svg: any, props: any, emit: any) {
  // Construct root node/hierarchy from the data
  root = d3.hierarchy(data)

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // Compute the layout - assigns x and y positions to the nodes
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Expand the root node to start with 1st level children visible
  toggleChildrenCollapse(nodes[0], root, svg, data, props, emit)

  // Render the nodes, links and extra links
  renderChildrenNodes(nodes, root, svg, data, props, emit)
  renderChildrenLinks(links, svg)
  renderChildrenExtraLinks(nodes, svg)
}

/**
 * Update the children graph
 * @param data The data to update the graph with
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to update the graph on
 * @param props The props of the component
 * @param emit The emit function of the component
 */
function updateChildrenGraph(data: any, root: any, svg: any, props: any, emit: any) {
  // Construct root node/hierarchy from the data - use expanded children to determine hierarchy
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.children : null))

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // Compute the layout - assigns x and y positions to the nodes
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Render the nodes, links and extra links
  renderChildrenNodes(nodes, root, svg, data, props, emit)
  renderChildrenLinks(links, svg)
  renderChildrenExtraLinks(nodes, svg)
}

/**
 * Render the nodes of the graph
 * @param nodes The nodes to render
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to render the nodes on
 * @param childrenHierarchyData The data of the children hierarchy
 * @param props The props of the component
 * @param emit The emit function of the component
 */
function renderChildrenNodes(
  nodes: any,
  root: any,
  svg: any,
  childrenHierarchyData: any,
  props: any,
  emit: any
) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node-children').data(nodes, (d: any) => d.data.id)

  // on enter, append a new node group and set the class
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node-children')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      // Prevent the click event from propagating to the parent nodes
      event.stopPropagation()
      toggleChildrenCollapse(d, root, svg, childrenHierarchyData, props, emit)
    })

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    .attr('fill', (d: any) => {
      if (d.data.dep) {
        return nodeDeprecatedColor
      } else {
        // if is root node
        if (d.data.id === childrenHierarchyData.id) {
          return nodeRootColor
        }
        return d.data.has_children ? nodeNormalColor : nodeNoParentsColor
      }
    })
    // set the cursor style based on the presence of children, if root, leave as default
    .attr('cursor', (d: any, i: number) =>
      i === 0 ? 'default' : d.data.has_children ? 'pointer' : 'default'
    )
    .attr('stroke', '#444')
    .attr('stroke-width', (d: any) => (d.data.has_children ? 2 : 0))

  // append text to the node
  nodeEnter
    // exclude the root node from the text
    .filter((d: any) => d.depth !== 0)
    .append('text')
    .attr('dy', '.35em')
    .text((d: any) => d.data.label)

  // merge the enter and update selections
  const nodeUpdate = nodeEnter.merge(nodeSelection)

  // node update
  nodeUpdate
    .attr('transform', (d: any) => `translate(${d.y},${d.x})`)
    // display the node based on the parent expanded state - this is to avoid the node being displayed when the parent is collapsed if has not been handled by the togglecollapse function (should not happen - but just in case)
    .style('display', (d: any) => (d.parent && !d.parent.data.expanded ? 'none' : null))

  // Update the text position based on the expanded state
  nodeUpdate
    .select('text')
    // display none if prop showLabels is false
    .style('display', props.showLabels ? 'block' : 'none')
    // x: root at 0 and children otherwise based on expanded state
    .attr('x', (d: any, i: number) => (i === 0 ? 0 : d.data.expanded ? -15 : 10))
    // y: root at -20 and children not changed
    .attr('y', (d: any, i: number) => (i === 0 ? -20 : 0))
    // text-anchor: root at middle and children based on expanded state
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
          if (d.data.id === childrenHierarchyData.id) {
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
          if (d.data.id === childrenHierarchyData.id) {
            return nodeRootColor
          }
          return d.data.has_children ? nodeNormalColor : nodeNoParentsColor
        }
      })
    )

  // remove the nodes that are no longer needed
  nodeSelection.exit().remove()
}

/**
 * Toggle the collapse of the children of a node
 * @param node The node to toggle the collapse
 * @param root The root element that holds the hierarchy data
 * @param svg The SVG element to update the graph on
 * @param childrenHierarchyData The data of the children hierarchy
 * @param props The props of the component
 * @param emit The emit function of the component
 */
async function toggleChildrenCollapse(
  node: any,
  root: any,
  svg: any,
  childrenHierarchyData: any,
  props: any,
  emit: any
) {
  if (!node.data.has_children) {
    // console.log('Node has no children:', node.data.label)
    return
  }

  if (!node.data.children) {
    // Fetch the children of the node
    const newNodeData = await fetchChildren(node.data, props.includeDeprecated)
    updateChildrenHierarchyData(node, newNodeData, childrenHierarchyData)
  } else {
    // if it is the root node, do not collapse
    if (node.data.id === childrenHierarchyData.id) {
      return
    }
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }
  // Call the update function to re-render the graph
  updateChildrenGraph(childrenHierarchyData, root, svg, props, emit)
}

/**
 * Update the children hierarchy data with the new data
 * @param node The node to update the children of
 * @param newNodeData The new data of the node
 * @param childrenHierarchyData The data of the children hierarchy
 */
function updateChildrenHierarchyData(node: any, newNodeData: any, childrenHierarchyData: any) {
  if (!newNodeData) {
    return
  }
  // Update the children of the node in the hierarchy data
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      if (newNodeData.children) {
        currentNode.children = newNodeData.children.map((child: any) => ({
          ...child,
          expanded: false,
          children: null
        }))
      }
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

/**
 * Render the extra links of the children graph
 * @param nodes The nodes to render the extra links for
 * @param svg The SVG element to render the extra links on
 */
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

/**
 * Render the links of the children graph
 * @param links The links to render
 * @param svg The SVG element to render the links on
 */
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
 * Custom diagonal function for the links
 * @param d The data of the link
 * @param offset The offset of the link (default 13)
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
