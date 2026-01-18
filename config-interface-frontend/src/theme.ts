export const theme = {
  colors: {
    primary: "#667eea",
    secondary: "#764ba2",
    background: "#1a1d23",
    cardBackground: "#282c34",
    text: "white",
  },
  spacing: {
    small: "8px",
    medium: "15px",
    large: "20px",
    xlarge: "30px",
    xxlarge: "40px",
  },
  borderRadius: {
    small: "8px",
    medium: "12px",
  },
  breakpoints: {
    mobile: "480px",
  },
  fontSizes: {
    base: "1.1rem",
    large: "1.8rem",
  },
  shadows: {
    light: "0 2px 8px rgba(0, 0, 0, 0.2)",
    medium: "0 4px 6px rgba(0, 0, 0, 0.1)",
  },
};

export type Theme = typeof theme;
