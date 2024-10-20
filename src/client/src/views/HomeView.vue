<script setup lang="ts">
import IconGraph from '../components/icons/IconGraph.vue'
</script>

<template>
  <div class="text-justify text-nav-background mb-16 lg:mx-40 mx-8">
    <section class="lg:mt-[120px] mt-20 mb-12">
      <h1 class="text-center lg:text-4xl font-bold text-3xl">
        Interactive Visualization of the ISO 15926-4 Reference Data Library
      </h1>
      <h2
        class="lg:text-2xl text-xl font-semibold lg:mt-[60px] mt-12 mb-2.5 relative before:content-[''] before:absolute before:bottom-[-10px] lg:before:w-1/4 before:w-3/4 before:h-[2px] before:bg-nav-background"
      >
        Overview: ISO and RDL
      </h2>
      <p class="text-block mt-[30px] lg:text-lg">
        The International Organization for Standardization (ISO) develops and publishes standards.
        The ISO 15926-4 standard has the title Industrial automation systems and integration —
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

    <section class="mb-16">
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
      class="mb-[60px] text-center relative p-12 before:content-[''] before:absolute lg:before:top-[-5px] before:top-[-2.5px] before:left-0 before:w-full before:h-[1.5px] before:bg-nav-background after:content-[''] after:absolute lg:after:bottom-[-5px] after:bottom-[-2.5px] after:left-0 after:w-full after:h-[1.5px] after:bg-nav-background"
    >
      <p class="lg:text-lg lg:mb-[40px] mb-[35px]">
        Click the button below to explore the interactive visualization
      </p>
      <router-link to="/graph" class="flex justify-center hover:bg-transparent">
        <button
          class="border-none bg-nav-background text-white lg:text-lg font-black lg:px-[120px] py-4 px-16 cursor-pointer hover:bg-gray-500 flex items-center justify-center lg:mb-12 mb-10 rounded-lg"
        >
          <IconGraph class="navbar-icon mr-2" />
          Graph
        </button>
      </router-link>
      <p class="lg:text-lg font-bold mb-[8px]">Navigating the Graph:</p>
      <p class="lg:text-lg max-w-[900px] mx-auto">
        The graph's left sidepane allows for search and filtering, and the right sidepane displays
        the RDF data of a selected node. Clicking on a node toggles collapsibility, while clicking
        on a node label shows it's details in the info sidepane. Please note that applying any
        filters will reset the graph's expansion.
      </p>
    </section>

    <section class="mb-[40px] text-center">
      <p class="lg:text-lg">
        Released in October 2024, this visualization was developed and designed by the following UWA
        students:<br />
        <strong class="lg:font-medium"
          >Cameron O'Neill, Heidi Leow, Paul Maingi, Ryan Dorman, Shuai Shao, Vinita Rathore</strong
        >
      </p>
    </section>

    <section class="text-center mb-12">
      <p>
        <span class="lg:text-xl text-lg font-bold">Questions?</span>
        <span class="lg:text-lg lg:ml-2 ml-1">Contact us at:</span>
        <a
          href="mailto:systemhealthlab@gmail.com"
          class="lg:ml-1 lg:text-lg text-blue-500 hover:underline hover:bg-transparent hover:text-nav-background cursor-pointer"
          >systemhealthlab@gmail.com</a
        >
      </p>
      <p class="lg:text-medium">
        The source code for this visualization is available at
        <a
          href="https://github.com/nlp-tlp/15926-4-RDL-CITS3200"
          target="_blank"
          class="text-blue-500 hover:underline hover:bg-transparent hover:text-nav-background cursor-pointer"
          >GitHub</a
        >.
      </p>
    </section>

    <section class="flex lg:flex-row flex-col justify-center items-center text-center mb-12">
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
          alt="University of Western Australia Natural & Technical Language
        Processing Group Logo"
        />
      </a>
    </section>

    <p class="mt-12 mb-10 font-small text-center">Last updated on 14 October 2024</p>

    <section class="text-center lg:text-base text-sm m-5">
      <p>
        <strong>Disclaimer:</strong> This project is not sponsored by the International Organization
        for Standardization (ISO). It is an initiative of
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
