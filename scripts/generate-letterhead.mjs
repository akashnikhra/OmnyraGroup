import { chromium } from "playwright";
import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  ImageRun,
  AlignmentType,
  Header,
  Footer,
  BorderStyle,
  TabStopType,
  VerticalPositionAlign,
  PageOrientation,
} from "docx";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PROJECT_ROOT = path.resolve(__dirname, "..");
const SVG_PATH = path.join(PROJECT_ROOT, "brand-materials", "logos", "icon-only.svg");
const PNG_PATH = path.join(PROJECT_ROOT, "brand-materials", "letterhead", "logo-temp.png");
const OUTPUT_PATH = path.join(PROJECT_ROOT, "brand-materials", "letterhead", "letterhead-a4.docx");

const COLORS = {
  hexBlue: "00A8E8",
  junction: "0077B6",
  chrome: "8B949E",
  steel: "C9D1D9",
  carbon: "0D1117",
  borderLight: "E8ECF0",
  white: "FFFFFF",
};

async function convertSvgToPng() {
  console.log("Converting SVG to PNG via Playwright...");

  const svgContent = fs.readFileSync(SVG_PATH, "utf-8");
  const dataUrl = `data:image/svg+xml;base64,${Buffer.from(svgContent).toString("base64")}`;

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 200, height: 200 },
    deviceScaleFactor: 2,
  });

  const html = `<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; padding: 0; background: transparent; }
    img { display: block; width: 200px; height: 200px; }
  </style>
</head>
<body>
  <img src="${dataUrl}" />
</body>
</html>`;

  await page.setContent(html, { waitUntil: "networkidle" });
  await page.waitForTimeout(500);

  const imgElement = page.locator("img");
  await imgElement.screenshot({ path: PNG_PATH, omitBackground: true });

  await browser.close();
  console.log(`PNG saved to ${PNG_PATH}`);
}

function createLetterhead(logoBuffer) {
  // A4 dimensions in twips
  const PAGE_WIDTH = 11906; // 210mm
  const PAGE_HEIGHT = 16838; // 297mm
  const MARGIN = 1134; // 2cm

  const doc = new Document({
    styles: {
      default: {
        document: {
          run: {
            font: "Calibri",
            size: 21, // 10.5pt
          },
        },
      },
    },
    sections: [
      {
        properties: {
          page: {
            size: {
              width: PAGE_WIDTH,
              height: PAGE_HEIGHT,
              orientation: PageOrientation.PORTRAIT,
            },
            margin: {
              top: MARGIN,
              bottom: MARGIN,
              left: MARGIN,
              right: MARGIN,
            },
            pageBorders: {
              top: {
                style: BorderStyle.SINGLE,
                size: 6, // 3pt (half-points)
                color: COLORS.hexBlue,
                space: 0,
              },
              bottom: {
                style: BorderStyle.SINGLE,
                size: 6, // 3pt
                color: COLORS.hexBlue,
                space: 0,
              },
              left: {
                style: BorderStyle.NONE,
                size: 0,
                color: "auto",
                space: 0,
              },
              right: {
                style: BorderStyle.NONE,
                size: 0,
                color: "auto",
                space: 0,
              },
            },
            pageNumbers: {
              start: 1,
            },
          },
        },
        headers: {
          default: new Header({
            children: [
              // Logo + company info row
              new Paragraph({
                spacing: { after: 100 },
                border: {
                  bottom: {
                    style: BorderStyle.SINGLE,
                    size: 2, // 1pt
                    color: COLORS.borderLight,
                    space: 4,
                  },
                },
                children: [
                  // Logo icon
                  new ImageRun({
                    data: logoBuffer,
                    transformation: {
                      width: 40,
                      height: 40,
                    },
                    type: "png",
                    verticalAlign: VerticalPositionAlign.CENTER,
                  }),
                  // Tab to right side
                  new TextRun({
                    text: "\t",
                    font: "Calibri",
                  }),
                  // Company name
                  new TextRun({
                    text: "OmnyraGroup™",
                    font: "Calibri",
                    size: 18, // 9pt
                    color: COLORS.chrome,
                    bold: true,
                  }),
                ],
              }),
              // Tagline
              new Paragraph({
                spacing: { after: 40 },
                tabStops: [
                  {
                    type: TabStopType.RIGHT,
                    position: PAGE_WIDTH - MARGIN * 2,
                  },
                ],
                children: [
                  new TextRun({ text: "\t" }),
                  new TextRun({
                    text: "Information Security Training & Risk Advisory",
                    font: "Calibri",
                    size: 14, // 7pt
                    color: COLORS.chrome,
                  }),
                ],
              }),
              // Website
              new Paragraph({
                spacing: { after: 0 },
                tabStops: [
                  {
                    type: TabStopType.RIGHT,
                    position: PAGE_WIDTH - MARGIN * 2,
                  },
                ],
                children: [
                  new TextRun({ text: "\t" }),
                  new TextRun({
                    text: "www.omnyragroup.online",
                    font: "Calibri",
                    size: 14, // 7pt
                    color: COLORS.steel,
                  }),
                ],
              }),
            ],
          }),
        },
        footers: {
          default: new Footer({
            children: [
              // Footer line
              new Paragraph({
                spacing: { before: 100, after: 100 },
                border: {
                  top: {
                    style: BorderStyle.SINGLE,
                    size: 2, // 1pt
                    color: COLORS.borderLight,
                    space: 4,
                  },
                },
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({
                    text: "OmnyraGroup™  |  Structure in Motion  |  www.omnyragroup.online",
                    font: "Calibri",
                    size: 14, // 7pt
                    color: COLORS.chrome,
                  }),
                ],
              }),
            ],
          }),
        },
        children: [
          // Date placeholder
          new Paragraph({
            spacing: { after: 200 },
            children: [
              new TextRun({
                text: "[Date]",
                font: "Calibri",
                size: 20, // 10pt
                color: COLORS.carbon,
              }),
            ],
          }),

          // Blank line
          new Paragraph({ spacing: { after: 200 } }),

          // Recipient placeholders
          new Paragraph({
            spacing: { after: 40 },
            children: [
              new TextRun({
                text: "[Recipient Name]",
                font: "Calibri",
                size: 20,
                color: COLORS.carbon,
              }),
            ],
          }),
          new Paragraph({
            spacing: { after: 40 },
            children: [
              new TextRun({
                text: "[Title]",
                font: "Calibri",
                size: 20,
                color: COLORS.carbon,
              }),
            ],
          }),
          new Paragraph({
            spacing: { after: 40 },
            children: [
              new TextRun({
                text: "[Company]",
                font: "Calibri",
                size: 20,
                color: COLORS.carbon,
              }),
            ],
          }),

          // Blank lines
          new Paragraph({ spacing: { after: 200 } }),
          new Paragraph({ spacing: { after: 200 } }),

          // Subject line
          new Paragraph({
            spacing: { after: 200 },
            children: [
              new TextRun({
                text: "Re: [Subject]",
                font: "Calibri",
                size: 22, // 11pt
                bold: true,
                color: COLORS.carbon,
              }),
            ],
          }),

          // Blank lines
          new Paragraph({ spacing: { after: 200 } }),
          new Paragraph({ spacing: { after: 200 } }),

          // Body placeholder lines (writing space)
          ...Array.from({ length: 18 }, (_, i) =>
            new Paragraph({
              spacing: { after: 200 },
              border: {
                bottom: {
                  style: BorderStyle.SINGLE,
                  size: 1,
                  color: "F0F0F0",
                  space: 4,
                },
              },
              children: [
                new TextRun({
                  text: " ",
                  font: "Calibri",
                  size: 20,
                }),
              ],
            })
          ),
        ],
      },
    ],
  });

  return doc;
}

async function main() {
  try {
    // Step 1: Convert SVG to PNG
    await convertSvgToPng();

    // Step 2: Read the PNG buffer
    const logoBuffer = fs.readFileSync(PNG_PATH);
    console.log(`Logo PNG loaded: ${logoBuffer.length} bytes`);

    // Step 3: Create the document
    const doc = createLetterhead(logoBuffer);

    // Step 4: Pack and save
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(OUTPUT_PATH, buffer);

    const stats = fs.statSync(OUTPUT_PATH);
    console.log(`Letterhead created: ${OUTPUT_PATH}`);
    console.log(`File size: ${(stats.size / 1024).toFixed(1)} KB`);

    // Cleanup temp PNG
    if (fs.existsSync(PNG_PATH)) {
      fs.unlinkSync(PNG_PATH);
      console.log("Cleaned up temporary PNG.");
    }

    console.log("\nDONE");
  } catch (err) {
    console.error("ERROR:", err);
    process.exit(1);
  }
}

main();
