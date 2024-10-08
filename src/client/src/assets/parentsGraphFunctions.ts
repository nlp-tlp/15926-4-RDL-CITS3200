import * as d3 from 'd3'

import { fetchParents } from "@/assets/apiFunctions"

const nodeRadius: number = 7
const nodeDistanceX: number = 25
const nodeDistanceY: number = 350


// draw the parents graph
function drawParentsGraph(data: any, root: any, svg: any, includeDeprecated: boolean) {
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
  toggleParentsCollapse(nodes[0], root, svg, data, includeDeprecated)

  // Render the nodes and links
  renderParentsNodes(nodes, root, svg, data, includeDeprecated)
  renderParentsLinks(links, svg)
  renderParentsExtraLinks(nodes, svg)
}

// update
function updateParentsGraph(data: any, root:any, svg: any, includeDeprecated: boolean) {
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.parents : null))

  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  const nodes = root.descendants()
  const links = root.links()

  renderParentsNodes(nodes, root, svg, data, includeDeprecated)
  renderParentsLinks(links, svg)
  renderParentsExtraLinks(nodes, svg)
}

// render the nodes of the graph - uses nodes array
function renderParentsNodes(nodes: any, root: any, svg: any, parentHierarchyData: any, includeDeprecated: boolean) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)
  // console.log('Nodes:', nodes)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      event.stopPropagation()
      toggleParentsCollapse(d, root, svg, parentHierarchyData, includeDeprecated)
    })

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    // set the fill color based on the presence of parents
    // .attr('fill', (d: any) => (d.data.has_parents ? '#69b3a2' : '#999'))
    .attr('fill', (d: any) => {
      if (d.data.dep) {
        return '#fc1455'
      } else {
        return d.data.has_parents ? '#69b3a2' : '#999'
      }
    })
    // set the cursor style based on the presence of parents
    .attr('cursor', (d: any) => (d.data.has_parents ? 'pointer' : 'default'))
    .attr('stroke', '#444')
    .attr('stroke-width', (d: any) => (d.data.has_parents ? 2 : 0))

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

    // x: root at 0 and parents otherwise based on expanded state
    .attr('x', (d: any, i: number) => (i === 0 ? 0 : d.data.expanded ? -15 : 10))
    // y: root at -20 and parents not changed
    .attr('y', (d: any, i: number) => (i === 0 ? -20 : 0))
    // text-anchor: root at middle and parents based on expanded state
    .style('text-anchor', (d: any, i: number) =>
      i === 0 ? 'middle' : d.data.expanded ? 'end' : 'start'
    )
    .style('font-weight', (d: any) => (d.data.dep ? 300 : 450))
    .style('font-style', (d: any) => (d.data.dep ? 'italic' : 'normal'))

  // remove the nodes that are no longer needed
  nodeSelection.exit().remove()
}


// toggle the collapse/expansion of a node
async function toggleParentsCollapse(node: any, root: any, svg: any, parentHierarchyData: any, includeDeprecated: boolean) {
  if (!node.data.has_parents) {
    console.log('Node has no parents:', node.data.label)
    return
  }

  if (!node.data.parents) {
    // Fetch the parents of the node
    const newNodeData = await fetchParents(node.data, includeDeprecated)
    updateParentsHierarchyData(node, newNodeData, parentHierarchyData)
  } else {
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }

  updateParentsGraph(parentHierarchyData, root, svg, includeDeprecated)
}

// find the node in parentHierarchyData and update it
function updateParentsHierarchyData(node: any, newNodeData: any, parentHierarchyData: any) {
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      currentNode.parents = newNodeData.parents.map((child: any) => ({
        ...child,
        expanded: false,
        parents: null
      }))
      currentNode.expanded = true
      return true
    }

    if (currentNode.parents) {
      for (const child of currentNode.parents) {
        if (updateNode(child)) {
          return true
        }
      }
    }

    return false
  }

  updateNode(parentHierarchyData)
}



// render the extra links of the graph
function renderParentsExtraLinks(nodes: any, svg: any) {
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
    const extraLink: any = svg.selectAll('path.extra-link').data(extraLinks, (d: any) => d.target.id)
  
    // on enter, insert the path element and set the attributes
    const extraLinkEnter = extraLink
      .enter()
      .insert('path', 'g')
      .attr('class', 'extra-link')
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
function renderParentsLinks(links: any, svg: any) {
    // Select all links and bind the data
    const link = svg.selectAll('path.link').data(links, (d: any) => d.target.id)
  
    // on enter, insert the path element and set the attributes
    const linkEnter = link
      .enter()
      .insert('path', 'g')
      .attr('class', 'link')
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
  const sourceX = d.source.y;
  const sourceY = d.source.x;
  const targetX = d.target.y;
  const targetY = d.target.x;

  // Determine if it's a forward or backward link
  const isForward = targetX > sourceX;

  // Check if the link is vertical or near-vertical
  if (Math.abs(sourceX - targetX) < 1) {
    // For vertical links, adjust the end point slightly to make arrow visible
    const arrowAdjustment = isForward ? -offset : offset;
    return `
      M ${sourceX},${sourceY}
      L ${targetX},${targetY + arrowAdjustment}
    `;
  }

  // For non-vertical links, apply offset and use a curved path
  const adjustedTargetX = isForward ? targetX - offset : targetX + offset;
  const midX = (sourceX + adjustedTargetX) / 2;
  return `
    M ${sourceX},${sourceY}
    C ${midX},${sourceY} ${midX},${targetY} ${adjustedTargetX},${targetY}
  `;
}




export { drawParentsGraph }