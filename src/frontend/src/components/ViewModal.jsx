import React, { useContext, useState } from 'react';
import link_image from "../images/link.jpg";
import screenshot_image from "../images/screenshot.jpg";
import notes_image from "../images/notes.png";
import SearchBar from "./SearchBar";
import SearchResults from "./SearchResults";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import "./style.css";
import { AppContext } from '../App';
import { Form, FormGroup } from 'react-bootstrap';

export default function ViewModal() {
  const {
    show,
    setShow,
    setView,
    view,
  } = useContext(AppContext);

  return (
    <Modal animation={false} show={show} onHide={() => setShow(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Change View</Modal.Title>
      </Modal.Header>
       <Modal.Body>Change view name:</Modal.Body>
       <input type="text" value={view} onChange={(e) => setView(e.target.value)}></input>
      <Modal.Footer>
        <Button variant="secondary" onClick={() => setShow(false)}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
    )
}
