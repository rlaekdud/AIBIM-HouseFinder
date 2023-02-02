import React, { useState } from "react";
import styled from "styled-components";

// component
import SelectInput from "./SelectInput";
import { Button } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRotate } from "@fortawesome/free-solid-svg-icons";

const Wrapper = styled.div`
  width: 100%;
`;

const ResetSection = styled.section`
  width: 90%;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10%;
`;

const RoomCondition = ({
  value,
  data,
  handleClassName,
  handleRoomRelation,
  handleResetOneRoomRelation,
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
    setCondition(data[className.find((it) => it === e)]);
  };

  return (
    <Wrapper>
      <ResetSection>
        <Button
          fullWidth
          size="xs"
          radius={"md"}
          style={{
            width: "45%",
            color: "#002060",
            border: "none",
            fontWeight: "bold",
            backgroundColor: "#EEEEEE",
          }}
          variant="outline"
          leftIcon={<FontAwesomeIcon icon={faRotate} />}
          onClick={handleResetOneRoomRelation}
        >
          Reset
        </Button>
      </ResetSection>
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
