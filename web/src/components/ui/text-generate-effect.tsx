"use client";

import { motion } from "motion/react";
import { cn } from "@/lib/utils";

/**
 * Reveals text word-by-word with a blur-in — adapted from Aceternity UI's
 * TextGenerateEffect. Fires the first time it scrolls into view.
 */
export function TextGenerateEffect({
  words,
  className,
  delay = 0,
  stagger = 0.05,
}: {
  words: string;
  className?: string;
  delay?: number;
  stagger?: number;
}) {
  const tokens = words.split(" ");
  return (
    <motion.span
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      transition={{ staggerChildren: stagger, delayChildren: delay }}
      className={cn("inline", className)}
    >
      {tokens.map((word, i) => (
        <motion.span
          key={`${word}-${i}`}
          variants={{
            hidden: { opacity: 0, filter: "blur(8px)", y: 6 },
            visible: { opacity: 1, filter: "blur(0px)", y: 0 },
          }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="inline-block"
        >
          {word}&nbsp;
        </motion.span>
      ))}
    </motion.span>
  );
}
