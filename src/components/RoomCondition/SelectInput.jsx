import React, { useState } from "react";
import { Select } from "@mantine/core";

const SelectInput = ({ value, data, placeholder, onChange }) => {
  return (
    <Select
      placeholder={placeholder}
      value={value}
      data={data}
      searchable
      nothingFound="No options"
      maxDropdownHeight={280}
      size={"lg"}
      style={{ width: "80%", marginBottom: "10%" }}
      radius={"md"}
      transition="pop-top-left"
      transitionDuration={80}
      transitionTimingFunction="ease"
      onChange={onChange}
    />
  );
};

export default React.memo(SelectInput);
