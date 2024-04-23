import "./style.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import MainPageContent from "./MainPageContent";
import React, { useState, useRef } from "react";

/**
 * 
 * The main component for showing search and config options.
 *
 * @returns {object} HTML object - The main page.
 */
export default function MainPage() {
  return (
    <div>
      <MainPageContent/>
    </div>);
}
