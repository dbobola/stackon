import styled from "styled-components";
import { Link } from "react-scroll";

export const Button = styled(Link)`
  border-radius: 50px;
  background: ${({ primary }) => (primary ? "#00bbf9" : "#010606")};
  white-space: nowrap;
  padding: ${({ padbig }) => (padbig ? "14px 48px" : "12px 12px")};
  color: ${({ dark }) => (dark ? "#010606" : "fff")};
  font-size: ${({ fontBig }) => (fontBig ? "18px" : "22px")};
  outline: none;
  border: none;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease-in-out;

  &:hover {
    transition: all 0.2s ease-in-out;
    background: ${({ hovprimary }) => (hovprimary ? "#02081f" : "#fff")};
    color: ${({ hovcolor }) => (hovcolor ? "#fff" : "black")};
  }
`;
