import React, { useState, useEffect } from "react";
import styled from "styled-components";

// component
import SelectInput from "./SelectInput";

const Wrapper = styled.div`
  width: 100%;
`;

const RoomCondition = ({
  value,
  data,
  handleClassName,
  handleRoomRelation,
}) => {
  // data -> classname에 따른 room condition 도출
  const className = Object.keys(data);

  // 선택된 roomRelation 저장
  const [condition, setCondition] = useState(() => {
    if (value.className) {
      return data[className.find((it) => it === value.className)];
    } else {
      return [];
    }
  });

  // className이 선택한 key에 해당하는 values 값 반환
  const selectCondition = (e) => {
    handleClassName(e);
    handleRoomRelation(e);
    setCondition(data[className.find((it) => it === e)]);
  };

  return (
    <Wrapper>
      <SelectInput
        placeholder={"ClassName"}
        value={value.className}
        data={className}
        onChange={selectCondition}
      />
      <SelectInput
        placeholder={"Room Relation"}
        value={value.roomRelation}
        data={condition}
        onChange={handleRoomRelation}
      />
    </Wrapper>
  );
};
export default React.memo(RoomCondition);
