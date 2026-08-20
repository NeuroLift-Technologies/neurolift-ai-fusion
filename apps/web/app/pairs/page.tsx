"use client";

import {
  ArrowRight,
  CheckCircle2,
  CircleDashed,
  Orbit,
  Search,
  Sparkles,
  X,
} from "lucide-react";
import {
  useDeferredValue,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
} from "react";
import styles from "./pairs.module.css";
import {
  avatarAidePairs,
  domainLabels,
  statusLabels,
  type AvatarAidePair,
  type PairDomain,
} from "./pairs";

type StatusFilter = "all" | "runtime-aligned" | "design-proposal";
type DomainFilter = "all" | PairDomain;

const statusFilters: { value: StatusFilter; label: string }[] = [
  { value: "all", label: "All 19" },
  { value: "runtime-aligned", label: "Runtime-aligned" },
  { value: "design-proposal", label: "Design proposals" },
];

const pairNumberById = new Map(avatarAidePairs.map((pair, index) => [pair.id, index + 1]));

function pairStyle(pair: AvatarAidePair) {
  return { "--pair-hue": pair.hue } as CSSProperties;
}

function matchesStatus(pair: AvatarAidePair, filter: StatusFilter) {
  if (filter === "all") return true;
  if (filter === "runtime-aligned") return pair.status !== "design-proposal";
  return pair.status === "design-proposal";
}

function PairGlyph({ pair, large = false }: { pair: AvatarAidePair; large?: boolean }) {
  return (
    <div className={large ? styles.pairGlyphLarge : styles.pairGlyph} style={pairStyle(pair)} aria-hidden="true">
      <span className={styles.avatarDisc}>{pair.tag}</span>
      <span className={styles.synapse}>
        <i />
      </span>
      <span className={styles.aideDisc}>A</span>
    </div>
  );
}

function StatusMark({ pair }: { pair: AvatarAidePair }) {
  if (pair.status === "runtime-pair") {
    return <CheckCircle2 size={13} strokeWidth={2.2} />;
  }

  return <CircleDashed size={13} strokeWidth={2.2} />;
}

export default function AvatarAidePairsPage() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [domainFilter, setDomainFilter] = useState<DomainFilter>("all");
  const [selectedId, setSelectedId] = useState(avatarAidePairs[0].id);
  const nodeRefs = useRef<Array<HTMLButtonElement | null>>([]);

  const filteredPairs = useMemo(() => {
    const normalizedQuery = deferredQuery.trim().toLowerCase();

    return avatarAidePairs.filter((pair) => {
      const searchable = [
        pair.name,
        pair.trait,
        pair.blurb,
        pair.aide.name,
        pair.aide.style,
        ...pair.aide.techniques,
      ]
        .join(" ")
        .toLowerCase();

      return (
        matchesStatus(pair, statusFilter) &&
        (domainFilter === "all" || pair.domain === domainFilter) &&
        (!normalizedQuery || searchable.includes(normalizedQuery))
      );
    });
  }, [deferredQuery, domainFilter, statusFilter]);

  const selectedPair = filteredPairs.find((pair) => pair.id === selectedId) ?? filteredPairs[0] ?? null;

  const handleNodeKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    if (!filteredPairs.length || !["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) {
      return;
    }

    event.preventDefault();
    const direction = event.key === "ArrowLeft" || event.key === "ArrowUp" ? -1 : 1;
    const nextIndex = (index + direction + filteredPairs.length) % filteredPairs.length;
    setSelectedId(filteredPairs[nextIndex].id);
    nodeRefs.current[nextIndex]?.focus();
  };

  return (
    <div className={styles.pageShell}>
      <div className={styles.ambientGlow} aria-hidden="true" />

      <header className={styles.hero}>
        <div className={styles.eyebrow}>
          <Orbit size={15} aria-hidden="true" />
          Pair atlas · v0.1
        </div>
        <div className={styles.heroGrid}>
          <div>
            <h1>
              Nineteen ways to <em>understand</em> and <span>support.</span>
            </h1>
            <p className={styles.intro}>
              Explore the one-to-one relationships at the heart of NeuroLift: an Avatar embodies a
              lived challenge, while its Aide brings a focused coaching response.
            </p>
          </div>
          <div className={styles.rosterSummary} aria-label="Roster implementation summary">
            <div>
              <strong>19</strong>
              <span>paired concepts</span>
            </div>
            <div>
              <strong>02</strong>
              <span>runtime-aligned</span>
            </div>
            <div>
              <strong>17</strong>
              <span>design proposals</span>
            </div>
          </div>
        </div>
      </header>

      <section className={styles.controls} aria-label="Filter the pair atlas">
        <div className={styles.searchField}>
          <Search size={17} aria-hidden="true" />
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search a trait, coach, or technique…"
            aria-label="Search Avatar-Aide pairs"
          />
          {query ? (
            <button type="button" onClick={() => setQuery("")} aria-label="Clear search">
              <X size={15} />
            </button>
          ) : null}
        </div>

        <div className={styles.statusFilters} aria-label="Filter by implementation status">
          {statusFilters.map((filter) => (
            <button
              key={filter.value}
              type="button"
              className={statusFilter === filter.value ? styles.filterActive : undefined}
              onClick={() => setStatusFilter(filter.value)}
              aria-pressed={statusFilter === filter.value}
            >
              {filter.label}
            </button>
          ))}
        </div>

        <label className={styles.domainField}>
          <span>Domain</span>
          <select value={domainFilter} onChange={(event) => setDomainFilter(event.target.value as DomainFilter)}>
            <option value="all">All domains</option>
            {Object.entries(domainLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>
      </section>

      <div className={styles.workspace}>
        <section className={styles.atlasPanel} aria-labelledby="atlas-heading">
          <div className={styles.sectionHeading}>
            <div>
              <span>Neural field</span>
              <h2 id="atlas-heading">Pair constellation</h2>
            </div>
            <p aria-live="polite">
              {filteredPairs.length.toString().padStart(2, "0")} / 19 visible
            </p>
          </div>

          {filteredPairs.length ? (
            <ol className={styles.constellation}>
              {filteredPairs.map((pair, index) => {
                const isSelected = selectedPair?.id === pair.id;
                return (
                  <li key={pair.id}>
                    <button
                      type="button"
                      ref={(node) => {
                        nodeRefs.current[index] = node;
                      }}
                      className={isSelected ? styles.nodeSelected : styles.node}
                      style={pairStyle(pair)}
                      onClick={() => setSelectedId(pair.id)}
                      onKeyDown={(event) => handleNodeKeyDown(event, index)}
                      aria-pressed={isSelected}
                      aria-label={`${pair.name} paired with ${pair.aide.name}: ${pair.trait}`}
                    >
                      <span className={styles.nodeIndex}>
                        {String(pairNumberById.get(pair.id)).padStart(2, "0")}
                      </span>
                      <PairGlyph pair={pair} />
                      <span className={styles.nodeCopy}>
                        <strong>{pair.name}</strong>
                        <small>{pair.trait}</small>
                      </span>
                      <span className={styles.nodeStatus} title={statusLabels[pair.status]}>
                        <StatusMark pair={pair} />
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
          ) : (
            <div className={styles.emptyState}>
              <Orbit size={34} aria-hidden="true" />
              <h3>No signals found</h3>
              <p>Try another search phrase or reset the atlas filters.</p>
              <button
                type="button"
                onClick={() => {
                  setQuery("");
                  setStatusFilter("all");
                  setDomainFilter("all");
                }}
              >
                Reset filters
              </button>
            </div>
          )}
        </section>

        <aside className={styles.detailColumn} aria-label="Selected pair details" aria-live="polite">
          {selectedPair ? (
            <div className={styles.detailCard} style={pairStyle(selectedPair)}>
              <div className={styles.detailTopline}>
                <span className={styles.detailNumber}>
                  Pair {String(pairNumberById.get(selectedPair.id)).padStart(2, "0")}
                </span>
                <span className={`${styles.statusBadge} ${styles[selectedPair.status]}`}>
                  <StatusMark pair={selectedPair} />
                  {statusLabels[selectedPair.status]}
                </span>
              </div>

              <div className={styles.pairStage}>
                <div className={styles.orbitRing} aria-hidden="true" />
                <PairGlyph pair={selectedPair} large />
                <span className={styles.stageLabel}>one-to-one support loop</span>
              </div>

              <div className={styles.identityGrid}>
                <div>
                  <span className={styles.roleLabel}>Avatar · experience</span>
                  <h2>{selectedPair.name}</h2>
                  <p className={styles.trait}>{selectedPair.trait}</p>
                  <p>{selectedPair.blurb}</p>
                </div>
                <div>
                  <span className={styles.roleLabel}>Aide · expertise</span>
                  <h2>{selectedPair.aide.name}</h2>
                  <p className={styles.trait}>{selectedPair.aide.style}</p>
                  <p>Offers a calibrated response without replacing the Avatar’s agency.</p>
                </div>
              </div>

              <div className={styles.responseFlow}>
                <div>
                  <span>Challenge signal</span>
                  <strong>{selectedPair.trait}</strong>
                </div>
                <ArrowRight size={19} aria-hidden="true" />
                <div>
                  <span>Coaching response</span>
                  <strong>{selectedPair.aide.style}</strong>
                </div>
              </div>

              <div className={styles.techniques}>
                <span className={styles.roleLabel}>Aide focus</span>
                <div>
                  {selectedPair.aide.techniques.map((technique) => (
                    <span key={technique}>{technique}</span>
                  ))}
                </div>
              </div>

              <div className={styles.domainNote}>
                <Sparkles size={16} aria-hidden="true" />
                <div>
                  <span>Support domain</span>
                  <strong>{domainLabels[selectedPair.domain]}</strong>
                </div>
              </div>

              {selectedPair.status === "avatar-implemented" ? (
                <p className={styles.caveat}>
                  TaskKickstart has a Python Avatar implementation; its dedicated Aide remains represented by
                  the browser prototype definition.
                </p>
              ) : null}
              {selectedPair.status === "design-proposal" ? (
                <p className={styles.caveat}>
                  This pair belongs to the canonical prototype roster and is not yet implemented in the Python
                  runtime.
                </p>
              ) : null}
            </div>
          ) : null}
        </aside>
      </div>

      <footer className={styles.pageNote}>
        <span>Data provenance</span>
        <p>
          Roster and pair definitions are adapted from the repository’s canonical World Engine prototype.
          Status labels reflect the current Python implementation boundary.
        </p>
      </footer>
    </div>
  );
}
