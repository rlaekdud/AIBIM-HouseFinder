import styled from "styled-components";

const Wrapper = styled.div``;

const StyledBluePrint = styled.div`
  width: 18em;
  height: 22em;
  border: 2px solid black;
  margin-bottom: 3%;
  background-image: ${(props) => props.backgroundImg};
  background-size: cover;
  background-position: center;
  cursor: pointer;
`;

const StyledSpan = styled.span`
  font-weight: bold;
`;

const BluePrint = ({ item, onClick }) => {
  return (
    <Wrapper>
      <StyledBluePrint
        onClick={() => onClick(item)}
        backgroundImg={`url(${require(`/Users/LEESEUNGYEOL/Desktop/AIBIM-HouseFinder/src/Img/${item}.png`)})`}
      />
      <StyledSpan>{item}</StyledSpan>
    </Wrapper>
  );
};

export default BluePrint;
