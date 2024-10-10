<script setup lang="ts">
import IconGraph from '../components/icons/IconGraph.vue'
</script>

<script lang="ts">
export default {
  data() {
    return {
      lastUpdated: ''
    }
  },
  created() {
    const today = new Date()
    this.lastUpdated = today.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })
  }
}
</script>

<template>
  <div class="text-justify text-nav-background mb-[70px] mx-8">
    <section class="lg:mt-[120px] mt-[90px] mb-[70px]">
      <h1 class="text-center lg:text-4xl font-bold text-3xl">
        Interactive Visualization of the ISO 15926-4 Reference Data Library
      </h1>
      <p class="mt-[50px] font-small">Last updated on {{ lastUpdated }}</p>
      <h2
        class="lg:text-2xl text-xl font-semibold mt-[40px] mb-[10px] relative before:content-[''] before:absolute before:bottom-[-10px] lg:before:w-1/4 before:w-3/4 before:h-[2px] before:bg-nav-background"
      >
        Overview: ISO and RDL
      </h2>
      <p class="text-block mt-[30px] lg:text-lg">
        The International Organization for Standardization (ISO) develops and publishes standards.
        ISO 15926-4 standard has the title Industrial automation systems and integration —
        Integration of life-cycle data for process plants including oil and gas production
        facilities Part 4: Core reference data. The Reference Data Library (RDL) described in ISO
        15926-4 is made available as a set of spreadsheets and through an endpoint at
        <a
          href="https://15926.org/"
          target="_blank"
          class="text-nav-background underline hover:no-underline hover:bg-transparent hover:text-blue-500 cursor-pointer"
          >15926.org</a
        >.
      </p>
    </section>

    <section class="mb-[110px]">
      <h2
        class="lg:text-2xl text-xl mb-[10px] font-semibold relative before:content-[''] before:absolute before:bottom-[-10px] lg:before:w-[30%] before:w-[90%] before:h-[2px] before:bg-nav-background"
      >
        Purpose of this Visualization
      </h2>
      <p class="text-block mt-[30px] lg:text-lg">
        The goal of this webpage is to allow users of the RDL to explore and understand the
        hierarchy and relationships between classes and their superclasses in the RDL.
      </p>
    </section>

    <section
      class="mb-[110px] text-center relative px-[50px] py-[50px] before:content-[''] before:absolute before:top-[-20px] before:left-0 before:w-full before:h-[2px] before:bg-nav-background after:content-[''] after:absolute after:bottom-[-20px] after:left-0 after:w-full after:h-[1px] after:bg-nav-background"
    >
      <p class="lg:text-lg mb-[60px]">
        Click the button below to explore the interactive visualization
      </p>
      <router-link to="/graph" class="flex justify-center hover:bg-transparent">
        <button
          class="border-none bg-nav-background text-white lg:text-lg font-black lg:px-[120px] py-[16px] px-[70px] cursor-pointer hover:bg-gray-500 flex items-center justify-center mb-[70px] rounded-lg"
        >
          <IconGraph class="navbar-icon mr-2" />
          Graph
        </button>
      </router-link>
      <p class="lg:text-lg font-bold mb-[8px]">Navigating the Graph:</p>
      <p class="lg:text-lg">
        Please note that clicking on a node will expand/collapse it, clicking on a node label will
        select it and show it's details in the right side pane, the right side pane shows the rdf
        information of a selected node, the left side pane allows you to search and filter the nodes
        in a graph, and applying filters will reset the graph expansion.
      </p>
    </section>

    <section class="mb-[100px] text-center">
      <p class="lg:text-lg">
        Released in October 2024, this visualization was developed and designed by the following UWA
        students:<br />
        <strong class="lg:font-medium"
          >Cameron O'Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, Vinita Rathore</strong
        >
      </p>
      <p class="lg:text-medium">
        The source code for this visualization is available on
        <a
          href="https://github.com/nlp-tlp/15926-4-RDL-CITS3200"
          target="_blank"
          class="text-nav-background underline hover:no-underline hover:bg-transparent hover:text-blue-500 cursor-pointer"
          >GitHub</a
        >.
      </p>
    </section>

    <section class="text-center mb-[80px]">
      <h3
        class="lg:text-3xl text-2xl font-bold relative before:content-[''] before:absolute before:bottom-[-20px] before:w-[75%] before:h-[2px] before:bg-nav-background before:left-1/2 before:transform before:-translate-x-1/2"
      >
        Questions?
      </h3>
      <p class="mt-[50px] mb-[20px] lg:text-xl text-lg">Contact us at:</p>
      <p>
        <a
          href="mailto:systemhealthlab@gmail.com"
          class="lg:text-lg text-blue-500 hover:underline hover:bg-transparent hover:text-nav-background cursor-pointer"
          >systemhealthlab@gmail.com</a
        >
      </p>
    </section>

    <section class="flex lg:flex-row flex-col justify-center items-center text-center mb-[50px]">
      <a
        href="https://www.uwa.edu.au/"
        class="inline-block hover:bg-transparent cursor-pointer"
        target="_blank"
      >
        <img
          src="/images/UWA Logo.png"
          class="max-w-[188px] lg:mr-[45px] lg:mb-[0px] mb-[20px]"
          alt="University of Western Australia Logo"
        />
      </a>
      <a
        href="https://nlp-tlp.org/"
        class="inline-block hover:bg-transparent cursor-pointer"
        target="_blank"
      >
        <img
          src="/images/nlp-tlp-logo.png"
          class="max-w-[90px]"
          alt="University of Western Australia Natural & Technical Language Processing Group Logo"
        />
      </a>
    </section>

    <section class="text-center lg:text-base text-sm">
      <h4 class="font-medium">Disclaimer:</h4>
      <p>
        This project is not sponsored by the International Organization for Standardization (ISO).
        It is an initiative of
        <a
          href="https://nlp-tlp.org/"
          target="_blank"
          class="text-nav-background underline hover:no-underline hover:bg-transparent hover:text-blue-500 cursor-pointer"
          >The University of Western Australia's NLP-TLP Group</a
        >
        and is intended to assist the ISO/TC 184/SC 4 WG3.
      </p>
    </section>
  </div>
</template>
