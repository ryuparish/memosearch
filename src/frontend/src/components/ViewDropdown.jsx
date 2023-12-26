import React, { useContext } from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import { AppContext } from "../App";

export default function ViewDropdown() {
  const {
    setView,
    view,
    views,
  } = useContext(AppContext)

  const viewList = [];
  for (let i = 0; i < views.length; ++i) {
    viewList.push(<Dropdown.Item onClick={() => setView(views[i])}>{view}</Dropdown.Item>);
  }

  return (
    <DropdownButton id="dropdown-basic-button" title="Dropdown button">
      {viewList}
    </DropdownButton>
  );
}
