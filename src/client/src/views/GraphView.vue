<template>
  <GraphVisualisation :data />
  <GraphSearchSidepane />
  <GraphInfoSidepane />
</template>

<script setup lang="ts">
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

const data = {
  id: 'root',
  label: 'Root Node',
  children: [
    {
      id: 'child1',
      label: 'Child 1',
      children: [
        {
          id: 'grandchild1',
          label: 'Grandchild 1',
          children: [
            {
              id: 'greatgrandchild1',
              label: 'Great Grandchild 1',
              children: [
                {
                  id: 'greatgreatgrandchild1',
                  label: 'Great-Great Grandchild 1'
                },
                {
                  id: 'greatgreatgrandchild2',
                  label: 'Great-Great Grandchild 2'
                }
              ]
            },
            {
              id: 'greatgrandchild2',
              label: 'Great Grandchild 2',
              children: [
                {
                  id: 'greatgreatgrandchild3',
                  label: 'Great-Great Grandchild 3'
                },
                {
                  id: 'greatgreatgrandchild4',
                  label: 'Great-Great Grandchild 4'
                }
              ]
            }
          ]
        },
        {
          id: 'grandchild2',
          label: 'Grandchild 2',
          children: [
            {
              id: 'greatgrandchild3',
              label: 'Great Grandchild 5'
            }
          ]
        }
      ]
    },
    {
      id: 'child2',
      label: 'Child 2',
      children: [
        {
          id: 'grandchild3',
          label: 'Grandchild 3',
          children: [
            {
              id: 'greatgrandchild4',
              label: 'Great Grandchild 6'
            }
          ]
        },
        {
          id: 'grandchild4',
          label: 'Grandchild 4',
          children: [
            {
              id: 'greatgrandchild5',
              label: 'Great Grandchild 7'
            },
            {
              id: 'greatgrandchild6',
              label: 'Great Grandchild 8'
            }
          ]
        }
      ]
    },
    {
      id: 'child3',
      label: 'Child 3',
      children: [
        {
          id: 'grandchild5',
          label: 'Grandchild 5',
          children: [
            {
              id: 'greatgrandchild7',
              label: 'Great Grandchild 9'
            }
          ]
        },
        {
          id: 'grandchild6',
          label: 'Grandchild 6',
          children: [
            {
              id: 'greatgrandchild8',
              label: 'Great Grandchild 10'
            }
          ]
        }
      ]
    },
    {
      id: 'child4',
      label: 'Child 4',
      children: [
        {
          id: 'grandchild7',
          label: 'Grandchild 7',
          children: [
            {
              id: 'greatgrandchild9',
              label: 'Great Grandchild 11',
              children: [
                {
                  id: 'greatgreatgrandchild5',
                  label: 'Great-Great Grandchild 5'
                },
                {
                  id: 'greatgreatgrandchild6',
                  label: 'Great-Great Grandchild 6'
                }
              ]
            }
          ]
        }
      ]
    },
    {
      id: 'child5',
      label: 'Child 5',
      children: [
        {
          id: 'grandchild8',
          label: 'Grandchild 8'
        },
        {
          id: 'grandchild9',
          label: 'Grandchild 9',
          children: [
            {
              id: 'greatgrandchild10',
              label: 'Great Grandchild 12'
            }
          ]
        }
      ]
    },
    {
      id: 'child6',
      label: 'Child 6',
      children: [
        {
          id: 'grandchild10',
          label: 'Grandchild 10'
        }
      ]
    },
    {
      id: 'child7',
      label: 'Child 7',
      children: [
        {
          id: 'grandchild11',
          label: 'Grandchild 11',
          children: [
            {
              id: 'greatgrandchild11',
              label: 'Great Grandchild 13'
            }
          ]
        }
      ]
    },
    {
      id: 'child8',
      label: 'Child 8',
      children: [
        {
          id: 'grandchild12',
          label: 'Grandchild 12',
          extra_parents: [{ id: 'child2' }]
        }
      ]
    },
    {
      id: 'child9',
      label: 'Child 9',
      children: [
        {
          id: 'grandchild13',
          label: 'Grandchild 13',
          children: [
            {
              id: 'greatgrandchild12',
              label: 'Great Grandchild 14'
            }
          ]
        },
        {
          id: 'grandchild14',
          label: 'Grandchild 14'
        }
      ]
    },
    {
      id: 'child10',
      label: 'Child 10',
      children: [
        {
          id: 'grandchild15',
          label: 'Grandchild 15',
          extra_parents: [{ id: 'child3' }]
        }
      ]
    },
    {
      id: 'child11',
      label: 'Child 11',
      children: [
        {
          id: 'grandchild16',
          label: 'Grandchild 16'
        }
      ]
    },
    {
      id: 'child12',
      label: 'Child 12',
      children: [
        {
          id: 'grandchild17',
          label: 'Grandchild 17',
          extra_parents: [{ id: 'child4' }]
        }
      ]
    },
    {
      id: 'child13',
      label: 'Child 13',
      children: [
        {
          id: 'grandchild18',
          label: 'Grandchild 18'
        }
      ]
    },
    {
      id: 'child14',
      label: 'Child 14',
      children: [
        {
          id: 'grandchild19',
          label: 'Grandchild 19'
        }
      ]
    },
    {
      id: 'child15',
      label: 'Child 15',
      children: [
        {
          id: 'grandchild20',
          label: 'Grandchild 20'
        }
      ]
    },
    {
      id: 'child16',
      label: 'Child 16',
      children: [
        {
          id: 'grandchild21',
          label: 'Grandchild 21'
        }
      ]
    },
    {
      id: 'child17',
      label: 'Child 17',
      children: [
        {
          id: 'grandchild22',
          label: 'Grandchild 22',
          children: [
            {
              id: 'greatgrandchild13',
              label: 'Great Grandchild 15'
            }
          ]
        }
      ]
    },
    {
      id: 'child18',
      label: 'Child 18',
      children: [
        {
          id: 'grandchild23',
          label: 'Grandchild 23'
        }
      ]
    },
    {
      id: 'child19',
      label: 'Child 19',
      children: [
        {
          id: 'grandchild24',
          label: 'Grandchild 24'
        }
      ]
    },
    {
      id: 'child20',
      label: 'Child 20',
      children: [
        {
          id: 'grandchild1',
          label: 'Grandchild 1',
          children: [
            {
              id: 'greatgrandchild1',
              label: 'Great Grandchild 1',
              children: [
                {
                  id: 'greatgreatgrandchild1',
                  label: 'Great-Great Grandchild 1'
                },
                {
                  id: 'greatgreatgrandchild2',
                  label: 'Great-Great Grandchild 2',
                  extra_parents: [{ id: 'greatgrandchild13' }, { id: 'greatgrandchild10' }]
                }
              ]
            },
            {
              id: 'greatgrandchild2',
              label: 'Great Grandchild 2',
              children: [
                {
                  id: 'greatgreatgrandchild3',
                  label: 'Great-Great Grandchild 3'
                },
                {
                  id: 'greatgreatgrandchild4',
                  label: 'Great-Great Grandchild 4'
                }
              ]
            }
          ]
        }
      ]
    },
    {
      id: 'child21',
      label: 'Child 21',
      children: [
        {
          id: 'grandchild26',
          label: 'Grandchild 26'
        }
      ]
    },
    {
      id: 'child22',
      label: 'Child 22',
      children: [
        {
          id: 'grandchild27',
          label: 'Grandchild 27'
        }
      ]
    },
    {
      id: 'child23',
      label: 'Child 23',
      children: [
        {
          id: 'grandchild28',
          label: 'Grandchild 28'
        }
      ]
    },
    {
      id: 'child24',
      label: 'Child 24',
      children: [
        {
          id: 'grandchild29',
          label: 'Grandchild 29'
        }
      ]
    },
    {
      id: 'child25',
      label: 'Child 25',
      children: [
        {
          id: 'grandchild30',
          label: 'Grandchild 30'
        }
      ]
    },
    {
      id: 'child26',
      label: 'Child 26',
      children: [
        {
          id: 'grandchild31',
          label: 'Grandchild 31'
        }
      ]
    },
    {
      id: 'child27',
      label: 'Child 27',
      children: [
        {
          id: 'grandchild32',
          label: 'Grandchild 32'
        }
      ]
    },
    {
      id: 'child28',
      label: 'Child 28',
      children: [
        {
          id: 'grandchild33',
          label: 'Grandchild 33'
        }
      ]
    },
    {
      id: 'child29',
      label: 'Child 29',
      children: [
        {
          id: 'grandchild34',
          label: 'Grandchild 34'
        }
      ]
    },
    {
      id: 'child30',
      label: 'Child 30',
      children: [
        {
          id: 'grandchild35',
          label: 'Grandchild 35'
        }
      ]
    },
    {
      id: 'child31',
      label: 'Child 31',
      children: [
        {
          id: 'grandchild36',
          label: 'Grandchild 36'
        }
      ]
    },
    {
      id: 'child32',
      label: 'Child 32',
      children: [
        {
          id: 'grandchild37',
          label: 'Grandchild 37'
        }
      ]
    },
    {
      id: 'child33',
      label: 'Child 33',
      children: [
        {
          id: 'grandchild38',
          label: 'Grandchild 38'
        }
      ]
    },
    {
      id: 'child34',
      label: 'Child 34',
      children: [
        {
          id: 'grandchild39',
          label: 'Grandchild 39'
        }
      ]
    },
    {
      id: 'child35',
      label: 'Child 35',
      children: [
        {
          id: 'grandchild40',
          label: 'Grandchild 40'
        }
      ]
    },
    {
      id: 'child36',
      label: 'Child 36',
      children: [
        {
          id: 'grandchild41',
          label: 'Grandchild 41'
        }
      ]
    },
    {
      id: 'child37',
      label: 'Child 37',
      children: [
        {
          id: 'grandchild42',
          label: 'Grandchild 42'
        }
      ]
    },
    {
      id: 'child38',
      label: 'Child 38',
      children: [
        {
          id: 'grandchild43',
          label: 'Grandchild 43'
        }
      ]
    },
    {
      id: 'child39',
      label: 'Child 39',
      children: [
        {
          id: 'grandchild44',
          label: 'Grandchild 44'
        }
      ]
    },
    {
      id: 'child40',
      label: 'Child 40',
      children: [
        {
          id: 'grandchild45',
          label: 'Grandchild 45'
        }
      ]
    },
    {
      id: 'child41',
      label: 'Child 41',
      children: [
        {
          id: 'grandchild46',
          label: 'Grandchild 46'
        }
      ]
    },
    {
      id: 'child42',
      label: 'Child 42',
      children: [
        {
          id: 'grandchild47',
          label: 'Grandchild 47'
        }
      ]
    },
    {
      id: 'child43',
      label: 'Child 43',
      children: [
        {
          id: 'grandchild48',
          label: 'Grandchild 48'
        }
      ]
    },
    {
      id: 'child44',
      label: 'Child 44',
      children: [
        {
          id: 'grandchild49',
          label: 'Grandchild 49'
        }
      ]
    },
    {
      id: 'child45',
      label: 'Child 45',
      children: [
        {
          id: 'grandchild50',
          label: 'Grandchild 50'
        }
      ]
    }
  ]
}
</script>

<style scoped></style>
