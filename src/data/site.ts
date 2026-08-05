import journal from "./journal.json";

export const site = {
  name: "Sapient Journal",
  title: "Columbia University | Sapient Journal",
  description:
    "Columbia University's undergraduate journal of biological anthropology. Founded in 2012 and run by Columbia students since.",
  url: "https://www.sapientjournal.com",
  email: "sapientjournal@gmail.com",
  submitFormUrl:
    "https://docs.google.com/forms/d/e/1FAIpQLSd1DvQEFuo8cyYmTOOicaKOVZ-CmfXPOFJT9VetIDnUF8-_Sg/viewform?usp=header",
  flyerUrl: "/files/sapient-flyer.pdf",
  credit:
    "Website designed by Max Rose Zimberg and Ruby Mustill. Inspired by prior web design by Sheryl Crespo.",
};

/** Matches the original Wix menu. SUBMIT and CONTACT were broken links on
 *  Wix (both pointed at the homepage root); here they reach the real
 *  sections they were meant to. */
export const nav = [
  { href: "/#about", label: "About" },
  { href: "/journal", label: "Journal" },
  { href: "/#submit", label: "Submit" },
  { href: "/editorial-board", label: "Editorial Board" },
  { href: "/hominin-hub", label: "The Hominin Hub" },
  { href: "/#contact", label: "Contact" },
];

export const topics = [
  { title: "Human Variation & Genetics", image: "/images/topics/topic-1.jpg" },
  { title: "Evolutionary History & Theory", image: "/images/topics/topic-2.jpg" },
  { title: "Primate Behavior & Ecology", image: "/images/topics/topic-3.jpg" },
  { title: "Paleo-Archaeology & Morphology", image: "/images/topics/topic-4.jpg" },
];

export const reasons = [
  { title: "Peer-Reviewed Feedback", image: "/images/why-peer-review.jpg" },
  { title: "A Platform For Your Writing", image: "/images/why-platform.jpg" },
  { title: "Student Leadership Positions", image: "/images/why-leadership.jpg" },
];

export const cycle = journal.cycle;
export const volumes = journal.volumes;
