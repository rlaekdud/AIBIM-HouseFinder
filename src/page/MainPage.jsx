import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import styled from "styled-components";

// components
import Header from "../components/Header";
import LogoImg from "../components/LogoImg";
import RoomCondition from "../components/RoomCondition/RoomCondition";
import Btn from "../components/Btn";
import { engDataSet, korDataSet } from "../components/dataSet";

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
  margin-bottom: 3%;
`;

const BtnSection = styled.section`
  display: flex;
  gap: 1em;
`;

const StyledSelect = styled.div`
  width: 100%;

  display: flex;
  justify-content: space-between;

  margin-bottom: 10%;
`;

const BottomSection = styled.section`
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
`;

const MainPage = ({
  dataSet,
  setDataSet,
  handleReset,
  data,
  setData,
  handleSubmit,
}) => {
  const navigator = useNavigate();
  // method
  const handleHome = () => {
    setDataSet(true);
    handleReset();
    navigator("/");
  };

  const onClick = () => {
    // 다음 페이지로 route
    // 해당 state로 관리되는 정보 넘겨주기
    //submitData -> request 보낼 데이터 쌍

    const submitData = data.filter((it) => it.roomRelation !== "");
    if (submitData.length > 0) {
      // roomRelation만 모아서 넘겨주기
      const roomRelations = [];
      submitData.map((item) => {
        roomRelations.push(item.roomRelation);
      });
      handleSubmit(roomRelations);
      navigator("/select");
    } else {
      alert("데이터를 선택해 주세요");
    }
  };

  // data 중 params 에 해당하는 index data 변경
  const handleClassName = (e, params) => {
    const copyArray = [...data];
    copyArray[params].className = e;
    setData(copyArray);
  };

  // className에 따른 RoomRelation
  const handleRoomRelation = (e, params) => {
    if (e) {
      const copyArray = [...data];
      copyArray[params].roomRelation = e;
      setData(copyArray);
    } else {
      // error 처리
      const copyArray = [...data];
      copyArray[params].roomRelation = "";
      setData(copyArray);
    }
  };

  const handleResetOneRoomRelation = (e, params) => {
    const copyArray = [...data];
    copyArray[params].className = "";
    copyArray[params].roomRelation = "";
    setData(copyArray);
  };

  // 다중 요소 넘겨주는 컴포넌트
  function repeatRoomCondition() {
    const arr = [];
    for (let i = 0; i < 6; i++) {
      arr.push(
        <RoomCondition
          data={dataSet ? korDataSet : engDataSet}
          value={data[i]}
          // classname 선택
          handleClassName={(e) => {
            handleClassName(e, i);
          }}
          // roomRelation 선택
          handleRoomRelation={(e) => {
            handleRoomRelation(e, i);
          }}
          //하나의 roomRelation 초기화
          handleResetOneRoomRelation={(e) => {
            handleResetOneRoomRelation(e, i);
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
              onClick={() => {
                setData(() => {
                  data.map((it) => {
                    it.className = "";
                    it.roomRelation = "";
                  });
                  return data;
                });
                setDataSet(true);
              }}
              width="5em"
              height="2.5em"
              item="KOR"
              fontSize="1em"
              borderRadius={"10px"}
            />
            <Btn
              onClick={() => {
                setData(() => {
                  data.map((it) => {
                    it.className = "";
                    it.roomRelation = "";
                  });
                  return data;
                });
                setDataSet(false);
              }}
              width="5em"
              height="2.5em"
              item="ENG"
              fontSize="1em"
              borderRadius={"10px"}
            />
          </BtnSection>
        </HeaderSection>
        <h2 style={{ color: "#002060", marginBottom: "7%" }}>
          Select your room type
        </h2>
        {/* select */}
        <StyledSelect>{repeatRoomCondition()}</StyledSelect>
        {/* submit */}
        <Btn
          onClick={onClick}
          width="12em"
          height="2.3em"
          item="Search"
          fontSize="1.5em"
          borderRadius={"20px"}
        />
        {/* bottom */}
        <BottomSection>
          <LogoImg />
        </BottomSection>
      </Section>
    </Wrapper>
  );
};
export default React.memo(MainPage);
