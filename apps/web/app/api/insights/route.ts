import { NextRequest, NextResponse } from "next/server";
import { PAIRS, type AvatarAidePair } from "@/lib/avatar-pairs-data";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const pairIdParam = searchParams.get("pairId");

  if (!pairIdParam) {
    return NextResponse.json({ error: "pairId is required" }, { status: 400 });
  }

  const pairId = parseInt(pairIdParam, 10);
  const pair = PAIRS.find((p) => p.id === pairId);

  if (!pair) {
    return NextResponse.json({ error: "Pair not found" }, { status: 404 });
  }

  const insight = generateInsight(pair);
  return NextResponse.json({ insight });
}

function generateInsight(pair: AvatarAidePair): string {
  const struggles = pair.avatarStruggles
    .map((s) => s.toLowerCase())
    .join(", ");
  const expertise = pair.aideExpertise
    .map((e) => e.toLowerCase())
    .join(" and ");
  const scenario = pair.exampleScenario.toLowerCase();

  return (
    `Avatar ${pair.avatarName} exhibits ${pair.trait.toLowerCase()} with struggles including ${struggles}. ` +
    `Aide ${pair.aideName} brings expertise in ${expertise || "specialized coaching strategies"}. ` +
    `The fusion insight: ${pair.shortDescription} ` +
    `When the Advocate ${pair.advocateName} engages, ${pair.advocateStrength.toLowerCase()} emerges as the primary leverage point — ` +
    `exemplified by ${scenario}.`
  );
}
