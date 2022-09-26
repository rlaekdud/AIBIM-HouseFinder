import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

// components

import BluePrint from "../components/BluePrint";
import Btn from "../components/Btn";
import Header from "../components/Header";
import { Pagination } from "@mantine/core";

const Wrapper = styled.div`
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
`;
const Section = styled.div`
  width: 91%;
  height: 80%;
`;
const HeaderSection = styled.section`
  width: 100%;
  margin-bottom: 3%;
`;
const PrintSection = styled.section`
  width: 100%;
  margin-bottom: 3%;
`;
const PaginationSection = styled.section`
  width: 100vw;
  height: 45vh;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 3%;
  margin-bottom: 7%;
`;

const CenterSection = styled.section`
  width: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
`;

const dummyData = [
  "20-498-1",
  "18-235-1",
  "18-279-1",
  "18-235-1",
  "20-498-1",
  "18-235-1",
  "130-124-1",
  "18-279-1",
  "130-124-1",
  "18-235-1",
  "124-616-1",
  "18-279-1",
  "124-616-1",
  "18-279-1",
  "20-498-1",
  "130-124-1",
  "20-573-1",
  "124-616-1",
  "124-616-1",
];

const SelectPage = ({
  handleReset,
  handleDataList,
  handleResultData,
  dataList,
}) => {
  const navigator = useNavigate();
  const [page, setPage] = useState(1);

  //method
  const handleHome = () => {
    handleReset();
    navigator("/");
  };

  const handleAddType = () => {
    //dataList 초기화
    handleDataList([]);
    navigator(-1);
  };

  const handleResult = (item) => {
    // result로 해당 이미지들 도출하기
    handleResultData(item);
    navigator("/result");
  };

  return (
    <Wrapper>
      <Section>
        <HeaderSection>
          <Header onClick={handleHome} />
        </HeaderSection>
        <PrintSection>
          <CenterSection>
            <PaginationSection>
              {/* dataList 출력 */}
              {dummyData
                .slice((page - 1) * 4, (page - 1) * 4 + 4)
                .map((item) => (
                  <BluePrint item={item} onClick={handleResult} />
                ))}
            </PaginationSection>
          </CenterSection>
          <CenterSection>
            <Pagination
              total={parseInt(dummyData.length / 4) + 1}
              onChange={setPage}
              page={page}
              initialPage={1}
              color={"gray"}
              size={"lg"}
            />
          </CenterSection>
        </PrintSection>
        <Btn
          onClick={handleAddType}
          width="9em"
          height="2.3em"
          item="+Add Type"
          fontSize="1.5em"
          borderRadius={"20px"}
          position={"center"}
        />
      </Section>
    </Wrapper>
  );
};
export default SelectPage;
