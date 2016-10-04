import React, { Component } from 'react';
import { Button, Col, Form, FormGroup, FormControl, Modal } from 'react-bootstrap';

export default class FolderEditModal extends Component{
  render(){
    return (
      <Modal {...this.props} bsSize="small" aria-labelledby="contained-modal-title-sm">
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-sm">Edit Folder</Modal.Title>
        </Modal.Header>
        <Modal.Body>
        <Form action="post" onSubmit={this.props.onSave} className="folder">

        <FormGroup>
          <Col><strong>Name: </strong>
            <FormControl
              name="folderName" value ={this.props.folderName} type="text" required = {true} placeholder="Enter Folder Name" onChange={this.props.handleFieldChange}
            />
          </Col>
        </FormGroup>

        <Modal.Footer>
          <FormGroup>
          <Button onClick={this.props.onHide}>Close</Button>
          <Button type="submit" className="btn btn-primary">Save</Button>
          </FormGroup>

        </Modal.Footer>
        </Form>
        </Modal.Body>

      </Modal>
    );
  }
}