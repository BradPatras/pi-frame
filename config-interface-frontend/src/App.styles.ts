import styled from "styled-components";

export const AppContainer = styled.div`
  text-align: center;
  background-color: ${({ theme }) => theme.colors.background};
  min-height: 100vh;
`;

export const Header = styled.header`
  background: linear-gradient(
    135deg,
    ${({ theme }) => theme.colors.primary} 0%,
    ${({ theme }) => theme.colors.secondary} 100%
  );
  padding: ${({ theme }) => theme.spacing.xlarge}
    ${({ theme }) => theme.spacing.large};
  color: ${({ theme }) => theme.colors.text};
  box-shadow: ${({ theme }) => theme.shadows.medium};
`;

export const HeaderTitle = styled.p`
  margin: 0;
  font-size: ${({ theme }) => theme.fontSizes.large};
  font-weight: 600;
  letter-spacing: 0.5px;
`;

export const Content = styled.div`
  max-width: 500px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.xxlarge}
    ${({ theme }) => theme.spacing.large};
  color: ${({ theme }) => theme.colors.text};
`;

export const Label = styled.label`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: ${({ theme }) => theme.spacing.medium};
  font-size: ${({ theme }) => theme.fontSizes.base};
  background-color: ${({ theme }) => theme.colors.cardBackground};
  padding: ${({ theme }) => theme.spacing.large} 25px;
  border-radius: ${({ theme }) => theme.borderRadius.medium};
  margin-bottom: ${({ theme }) => theme.spacing.large};
  box-shadow: ${({ theme }) => theme.shadows.light};
  transition:
    transform 0.2s,
    box-shadow 0.2s;

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  span {
    flex: 0 0 auto;
  }
`;

export const InputGroup = styled.div`
  display: flex;
  gap: ${({ theme }) => theme.spacing.small};
  flex: 0 0 auto;
`;

export const NumberInput = styled.input`
  width: 5ch;
  padding: 10px 8px;
  font-size: ${({ theme }) => theme.fontSizes.base};
  text-align: center;
  border: 2px solid ${({ theme }) => theme.colors.primary};
  border-radius: ${({ theme }) => theme.borderRadius.small};
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.text};
  outline: none;
  transition: border-color 0.2s;

  &:focus {
    border-color: ${({ theme }) => theme.colors.secondary};
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: 1rem;
  }
`;

export const WideNumberInput = styled(NumberInput)`
  width: 100%;
  max-width: 400px;
  text-align: left;
  padding: 10px 15px;
`;

export const Select = styled.select`
  padding: 10px 15px;
  font-size: ${({ theme }) => theme.fontSizes.base};
  border: 2px solid ${({ theme }) => theme.colors.primary};
  border-radius: ${({ theme }) => theme.borderRadius.small};
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.text};
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;

  &:focus {
    border-color: ${({ theme }) => theme.colors.secondary};
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: 1rem;
  }
`;

export const UploadSection = styled.div`
  margin-top: ${({ theme }) => theme.spacing.xlarge};
  padding: ${({ theme }) => theme.spacing.large};
  background-color: ${({ theme }) => theme.colors.cardBackground};
  border-radius: ${({ theme }) => theme.borderRadius.medium};
  box-shadow: ${({ theme }) => theme.shadows.light};
`;

export const StyledUploadButton = styled.button`
  padding: 15px 30px;
  font-size: ${({ theme }) => theme.fontSizes.base};
  font-weight: 600;
  color: white;
  background: linear-gradient(
    135deg,
    ${({ theme }) => theme.colors.primary} 0%,
    ${({ theme }) => theme.colors.secondary} 100%
  );
  border: none;
  border-radius: ${({ theme }) => theme.borderRadius.small};
  cursor: pointer;
  outline: none;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  box-shadow: ${({ theme }) => theme.shadows.light};
  width: 100%;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  &:active {
    transform: translateY(0);
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    font-size: 1rem;
    padding: 12px 24px;
  }
`;
