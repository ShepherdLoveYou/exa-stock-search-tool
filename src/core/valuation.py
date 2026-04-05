"""
Crisis Investment Valuation Engine
10+ methods for cross-validation as required by the framework
"""

from typing import Dict, List


class ValuationMethods:
    """
    Collection of valuation calculation utilities
    Supports 10+ methods for cross-validation as required by the framework
    """

    @staticmethod
    def dcf(
        fcf_current: float,
        growth_rate: float,
        terminal_growth: float = 0.03,
        discount_rate: float = 0.10,
        years: int = 10,
        shares_outstanding: float = 1.0,
    ) -> Dict:
        """Discounted Cash Flow valuation"""
        projected_fcf = []
        fcf = fcf_current
        for yr in range(1, years + 1):
            fcf = fcf * (1 + growth_rate)
            pv = fcf / ((1 + discount_rate) ** yr)
            projected_fcf.append({"year": yr, "fcf": round(fcf, 2), "pv": round(pv, 2)})

        terminal_value = (
            fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        )
        terminal_pv = terminal_value / ((1 + discount_rate) ** years)

        total_pv = sum(item["pv"] for item in projected_fcf) + terminal_pv
        per_share = total_pv / shares_outstanding if shares_outstanding > 0 else 0

        return {
            "method": "DCF自由现金流折现",
            "total_enterprise_value": round(total_pv, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "fcf_current": fcf_current,
                "growth_rate": f"{growth_rate:.1%}",
                "terminal_growth": f"{terminal_growth:.1%}",
                "discount_rate": f"{discount_rate:.1%}",
                "projection_years": years,
            },
        }

    @staticmethod
    def graham_formula(eps: float, growth_rate: float, aaa_yield: float = 0.045) -> Dict:
        """Benjamin Graham intrinsic value formula: V = EPS * (8.5 + 2g) * 4.4 / Y"""
        g = growth_rate * 100
        value = eps * (8.5 + 2 * g) * 4.4 / (aaa_yield * 100)
        return {
            "method": "格雷厄姆公式",
            "per_share_value": round(value, 2),
            "assumptions": {
                "eps": eps,
                "growth_rate": f"{growth_rate:.1%}",
                "aaa_bond_yield": f"{aaa_yield:.1%}",
            },
        }

    @staticmethod
    def pe_relative(eps: float, industry_pe: float, premium: float = 1.0) -> Dict:
        """PE ratio relative valuation"""
        value = eps * industry_pe * premium
        return {
            "method": "PE市盈率对标",
            "per_share_value": round(value, 2),
            "assumptions": {
                "eps": eps,
                "industry_pe": industry_pe,
                "premium_factor": premium,
            },
        }

    @staticmethod
    def pb_relative(bvps: float, industry_pb: float) -> Dict:
        """PB ratio relative valuation"""
        value = bvps * industry_pb
        return {
            "method": "PB市净率对标",
            "per_share_value": round(value, 2),
            "assumptions": {"book_value_per_share": bvps, "industry_pb": industry_pb},
        }

    @staticmethod
    def ps_relative(revenue_per_share: float, industry_ps: float) -> Dict:
        """PS ratio relative valuation"""
        value = revenue_per_share * industry_ps
        return {
            "method": "PS市销率对标",
            "per_share_value": round(value, 2),
            "assumptions": {
                "revenue_per_share": revenue_per_share,
                "industry_ps": industry_ps,
            },
        }

    @staticmethod
    def ev_ebitda(
        ebitda: float,
        industry_multiple: float,
        net_debt: float,
        shares_outstanding: float,
    ) -> Dict:
        """EV/EBITDA enterprise value valuation"""
        ev = ebitda * industry_multiple
        equity_value = ev - net_debt
        per_share = equity_value / shares_outstanding if shares_outstanding > 0 else 0
        return {
            "method": "EV/EBITDA企业价值倍数",
            "enterprise_value": round(ev, 2),
            "equity_value": round(equity_value, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "ebitda": ebitda,
                "industry_multiple": industry_multiple,
                "net_debt": net_debt,
            },
        }

    @staticmethod
    def peg(eps: float, growth_rate: float, target_peg: float = 1.0) -> Dict:
        """PEG ratio valuation"""
        g = growth_rate * 100
        fair_pe = target_peg * g
        value = eps * fair_pe
        return {
            "method": "PEG估值法",
            "per_share_value": round(value, 2),
            "fair_pe": round(fair_pe, 1),
            "assumptions": {
                "eps": eps,
                "growth_rate": f"{growth_rate:.1%}",
                "target_peg": target_peg,
            },
        }

    @staticmethod
    def owner_earnings_valuation(
        owner_earnings: float,
        growth_rate: float,
        discount_rate: float = 0.10,
        shares_outstanding: float = 1.0,
    ) -> Dict:
        """Warren Buffett owner earnings valuation"""
        if discount_rate <= growth_rate:
            cap_rate = discount_rate + 0.02
        else:
            cap_rate = discount_rate - growth_rate

        value = owner_earnings / cap_rate
        per_share = value / shares_outstanding if shares_outstanding > 0 else 0
        return {
            "method": "股东盈余估值法",
            "total_value": round(value, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "owner_earnings": owner_earnings,
                "growth_rate": f"{growth_rate:.1%}",
                "discount_rate": f"{discount_rate:.1%}",
            },
        }

    @staticmethod
    def ddm(
        dividend_per_share: float,
        growth_rate: float,
        required_return: float = 0.10,
    ) -> Dict:
        """Dividend Discount Model (Gordon Growth)"""
        if required_return <= growth_rate:
            return {
                "method": "DDM股利折现模型",
                "per_share_value": None,
                "note": "Required return must exceed growth rate",
            }

        value = dividend_per_share * (1 + growth_rate) / (required_return - growth_rate)
        return {
            "method": "DDM股利折现模型",
            "per_share_value": round(value, 2),
            "assumptions": {
                "dividend_per_share": dividend_per_share,
                "growth_rate": f"{growth_rate:.1%}",
                "required_return": f"{required_return:.1%}",
            },
        }

    @staticmethod
    def replacement_cost(total_assets: float, intangibles: float, liabilities: float, shares: float) -> Dict:
        """Replacement/liquidation cost valuation"""
        nav = total_assets - intangibles - liabilities
        per_share = nav / shares if shares > 0 else 0
        return {
            "method": "重置成本法",
            "net_asset_value": round(nav, 2),
            "per_share_value": round(per_share, 2),
            "assumptions": {
                "total_assets": total_assets,
                "intangibles_excluded": intangibles,
                "total_liabilities": liabilities,
            },
        }

    @staticmethod
    def cross_validate(valuations: List[Dict]) -> Dict:
        """
        Cross-validate multiple valuation results.
        Flags methods whose inputs lack source citations.
        Returns median, mean, range, confidence, and source audit.
        """
        valid = []
        unsourced_methods = []

        for v in valuations:
            pv = v.get("per_share_value")
            if pv is None or pv <= 0:
                continue
            # Check if this valuation has source info
            assumptions = v.get("assumptions", {})
            has_source = bool(v.get("input_sources")) or any(
                "source" in str(val).lower() for val in assumptions.values()
            )
            valid.append({"value": pv, "method": v.get("method", "?"), "sourced": has_source})
            if not has_source:
                unsourced_methods.append(v.get("method", "?"))

        if not valid:
            return {"error": "No valid valuations to cross-validate"}

        values = [item["value"] for item in valid]
        values_sorted = sorted(values)
        n = len(values_sorted)
        median = (
            values_sorted[n // 2]
            if n % 2 == 1
            else (values_sorted[n // 2 - 1] + values_sorted[n // 2]) / 2
        )

        mean = sum(values) / n
        spread = (max(values) - min(values)) / median if median > 0 else 0

        confidence = "high" if spread < 0.3 else "medium" if spread < 0.6 else "low"

        # Downgrade confidence if many methods lack source citations
        if unsourced_methods:
            ratio_unsourced = len(unsourced_methods) / n
            if ratio_unsourced > 0.5 and confidence == "high":
                confidence = "medium"
            if ratio_unsourced > 0.5:
                confidence += " ⚠️ 多数估值方法的输入参数缺少来源标注"

        result = {
            "method_count": n,
            "median": round(median, 2),
            "mean": round(mean, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "spread": f"{spread:.1%}",
            "confidence": confidence,
            "all_values": [round(v, 2) for v in values_sorted],
        }

        if unsourced_methods:
            result["source_audit"] = {
                "unsourced_methods": unsourced_methods,
                "warning": (
                    f"{len(unsourced_methods)}/{n} 种估值方法的输入参数未标注数据来源。"
                    "存在使用记忆数据（幻觉）的风险。请为每个输入参数补充 input_sources。"
                ),
            }

        return result
