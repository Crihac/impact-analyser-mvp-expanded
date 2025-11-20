from graph.dependency_graph import GRAPH, FILE_TO_MODULE, MODULE_METADATA
from analyzer.risk_engine import calculate_risk
import networkx as nx

def analyze_impact(changed_files: list, repo_map: dict = None):
    G = nx.DiGraph()
    for src, targets in GRAPH.items():
        for t in targets:
            G.add_edge(src, t)

    impacted = []

    for f in changed_files:
        # if file maps to module directly even if node not in graph
        if f in FILE_TO_MODULE and f not in G.nodes:
            module = FILE_TO_MODULE[f]
            meta = MODULE_METADATA.get(module, {})
            risk = calculate_risk(0, meta)
            impacted.append({
                "module": module,
                "distance": 0,
                "risk": risk,
                "reason": f"Changed file maps directly to {module}",
                "meta": meta,
            })
            continue

        if f not in G.nodes:
            # unknown file -- attempt best-effort token mapping via repo_map
            if repo_map:
                mapped = repo_map.get('files_to_modules', {}).get(f)
                if mapped:
                    meta = MODULE_METADATA.get(mapped, {})
                    risk = calculate_risk(0, meta)
                    impacted.append({
                        "module": mapped,
                        "distance": 0,
                        "risk": risk,
                        "reason": f"Changed file maps via repo_map to {mapped}",
                        "meta": meta,
                    })
            continue

        lengths = nx.single_source_shortest_path_length(G, f, cutoff=3)
        for node, dist in lengths.items():
            # map node (file) to module
            module = FILE_TO_MODULE.get(node)
            if not module:
                continue
            meta = MODULE_METADATA.get(module, {})
            # use 0 distance for the file itself
            dist_for_risk = 0 if node == f else dist
            risk = calculate_risk(dist_for_risk, meta)
            impacted.append({
                "module": module,
                "distance": dist,
                "risk": risk,
                "reason": f"Reachable from {f} at distance {dist}",
                "meta": meta,
            })

    # merge by module keeping highest risk and collect reasons
    merged = {}
    for it in impacted:
        m = it['module']
        if m not in merged or it['risk'] > merged[m]['risk']:
            merged[m] = it
            merged[m]['reasons'] = [it['reason']]
        elif it['risk'] == merged[m]['risk']:
            merged[m]['reasons'].append(it['reason'])

    impacts = list(merged.values())
    overall_risk = round(max((i['risk'] for i in impacts), default=0), 2)

    return {
        "changed_files": changed_files,
        "overall_risk": overall_risk,
        "impacted_modules": impacts
    }
