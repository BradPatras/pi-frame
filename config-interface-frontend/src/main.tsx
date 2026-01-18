import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider } from "styled-components";
import { GlobalStyles } from "./GlobalStyles";
import { theme } from "./theme";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <App />
    </ThemeProvider>
  </StrictMode>,
);
