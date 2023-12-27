import React, { useContext } from 'react';
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
