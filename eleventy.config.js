export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy("src/reset.css");
  eleventyConfig.addPassthroughCopy("src/styles.css");
  eleventyConfig.addPassthroughCopy("src/app.js");
  eleventyConfig.addPassthroughCopy("src/calculator.js");

  eleventyConfig.addFilter("formatPrice", (value) =>
    new Intl.NumberFormat("ru-RU").format(value),
  );

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "dist",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
}
