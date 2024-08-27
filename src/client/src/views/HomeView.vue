<script setup lang="ts"></script>

<template>
  <h1>Interactive Visualization of the ISO 15926-4 Reference Data Library</h1>
  <br />
  <p>
    The International Organization for Standardization (ISO) is a globally recognized entity that
    develops and publishes standards across various industries. The ISO 15926-4 standard aims to
    facilitate digital data exchange across various phases of an industrial process plant’s life
    cycle by defining data in a standardized dictionary of classes. Specifically, the Reference Data
    Library (RDL) described in ISO 15926-4 is used to describe equipment, materials, and their
    attributes in a consistent and interoperable manner across different systems and
    organizations.<br /><br />Currently, the immediate relationships between classes and their
    superclasses are shown in the RDL, but there isn't a more holistic way of viewing the data such
    that the overall hierarchy can be easily seen. Therefore, this visualization was developed for
    the RDL as a hierarchical tree of classes to allow users to interrogate the data and to
    intuitively explore the hierarchy.
  </p>
  <br />
  <p>Click the button below to explore the interactive visualization:</p>
  <br />
  <router-link to="/graph">
    <button>Graph</button>
  </router-link>
  <br />
  <br />
  <p>
    This is a collaborative project between the International Organization for Standardization
    committee? and the University of Western Australia (UWA)
  </p>
  <br />
  <p>
    This interactive visualization tool was developed and designed by the following UWA students:<br />
    Cameron O'Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, Vinita Rathore
  </p>
</template>

<script setup lang="ts"></script>

<style scoped></style>
