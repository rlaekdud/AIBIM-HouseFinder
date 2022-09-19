import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import styled from "styled-components";

// components
import Header from "../components/Header";
import LogoImg from "../components/LogoImg";
import RoomCondition from "../components/RoomCondition/RoomCondition";
import Btn from "../components/Btn";
import { korDataSet } from "../components/dataSet";

//styled-component

const Wrapper = styled.div`
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
`;
// 화면 당 비율 조절
const Section = styled.section`
  width: 91%;
  height: 80%;
`;
const HeaderSection = styled.section`
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-bottom: 8%;
`;

const BtnSection = styled.section`
  display: flex;
  gap: 1em;
  margin-top: 2em;
`;

const StyledSelect = styled.div`
  width: 100%;

  display: flex;
  justify-content: space-between;

  margin-bottom: 10%;
`;

const BottomSection = styled.section`
  width: 100%;
  display: flex;
  margin-left: 5%;
  justify-content: flex-end;
  align-items: flex-end;
`;

const defaultData = [
  {
    id: 0,
    className: "",
    roomRelation: "",
  },
  {
    id: 1,
    className: "",
    roomRelation: "",
  },
  {
    id: 2,
    className: "",
    roomRelation: "",
  },
  {
    id: 3,
    className: "",
    roomRelation: "",
  },
  {
    id: 4,
    className: "",
    roomRelation: "",
  },
  {
    id: 5,
    className: "",
    roomRelation: "",
  },
];

const MainPage = ({ handleDataList }) => {
  const navigator = useNavigate();

  // className에 따른 RoomRelation
  // const [className, setClassName] = useState();

  // method
  const handleHome = () => {
    handleDataList();
    navigator("/");
  };

  const onClick = () => {
    // 다음 페이지로 route
    // 해당 state로 관리되는 정보 넘겨주기 -> how ???
    const submitData = result.filter((it) => it.roomRelation !== "");
    if (submitData.length > 0) {
      alert(`${JSON.stringify(submitData)} ${submitData.length}`);
      navigator("/select");
    } else {
      alert("데이터를 선택해 주세요");
    }
    // 최종 데이터 저장 localStorage에 저장
    handleDataList(JSON.stringify(submitData));
  };

  const handleClassName = (e, params) => {
    // const copyArray = [...result];
    // copyArray[params].className = e;
    // setClassName(copyArray);
  };

  const handleRoomRelation = (e, params) => {
    if (e) {
      const copyArray = [...result];
      copyArray[params].roomRelation = e;
      setResult(copyArray);
    } else {
      const copyArray = [...result];
      copyArray[params].roomRelation = "";
      setResult(copyArray);
    }
  };

  // 다중 요소 넘겨주는 컴포넌트
  function repeatRoomCondition() {
    const arr = [];
    for (let i = 0; i < 6; i++) {
      arr.push(
        <RoomCondition
          data={korDataSet}
          value={result[i]}
          handleClassName={(e) => {
            handleClassName(e, i);
          }}
          handleRoomRelation={(e) => {
            handleRoomRelation(e, i);
          }}
        />
      );
    }
    return arr;
  }

  return (
    <Wrapper>
      <Section>
        <HeaderSection>
          {/* LandingPage로 */}
          <Header onClick={handleHome} />
          {/* 언어변경 */}
          <BtnSection>
            <Btn
              onClick={() => {}}
              width="5em"
              height="2.5em"
              item="KOR"
              fontSize="1em"
              borderRadius={"10px"}
            />
            <Btn
              onClick={() => {}}
              width="5em"
              height="2.5em"
              item="ENG"
              fontSize="1em"
              borderRadius={"10px"}
            />
          </BtnSection>
        </HeaderSection>
        <h2 style={{ color: "#002060", marginBottom: "3%" }}>
          Select your room type
        </h2>
        <StyledSelect>{repeatRoomCondition()}</StyledSelect>
        <Btn
          onClick={onClick}
          width="12em"
          height="2.3em"
          item="search"
          fontSize="1.5em"
          borderRadius={"20px"}
        />
        <BottomSection>
          <LogoImg />
        </BottomSection>
      </Section>
    </Wrapper>
  );
};
export default React.memo(MainPage);
