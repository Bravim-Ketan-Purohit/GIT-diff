"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

/** Cycling typewriter — types each phrase, pauses, deletes, moves on. */
export function Typewriter({
  words,
  className,
  caretClassName,
  typingSpeed = 65,
  deletingSpeed = 30,
  pause = 1600,
}: {
  words: string[];
  className?: string;
  caretClassName?: string;
  typingSpeed?: number;
  deletingSpeed?: number;
  pause?: number;
}) {
  const [index, setIndex] = useState(0);
  const [text, setText] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = words[index % words.length];

    if (!deleting && text === current) {
      const t = setTimeout(() => setDeleting(true), pause);
      return () => clearTimeout(t);
    }
    if (deleting && text === "") {
      setDeleting(false);
      setIndex((i) => i + 1);
      return;
    }
    const t = setTimeout(
      () => setText(current.slice(0, deleting ? text.length - 1 : text.length + 1)),
      deleting ? deletingSpeed : typingSpeed,
    );
    return () => clearTimeout(t);
  }, [text, deleting, index, words, pause, typingSpeed, deletingSpeed]);

  return (
    <span className={cn(className)}>
      {text}
      <span className={cn("animate-blink font-normal text-brand", caretClassName)}>▌</span>
    </span>
  );
}
