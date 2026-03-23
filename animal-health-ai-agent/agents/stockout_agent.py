import pandas as pd


class StockoutAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)

    def analyze(self):
        df = self.df.copy()

        # Fulfillment ratio
        df["fulfillment_ratio"] = df["inventory_level"] / (df["sales_orders"] + 1)

        # Identify stockout risk
        df["stockout_risk"] = df["fulfillment_ratio"] < 0.5

        # High risk products
        high_risk_products = (
            df[df["stockout_risk"]]
            .groupby(["manufacturer", "product"])["inventory_level"]
            .sum()
            .sort_values(ascending=True)
        )
        high_risk_products_dict = {
            f"{manufacturer} | {product}": int(value)
            for (manufacturer, product), value in high_risk_products.to_dict().items()
        }

        # High risk manufacturers
        high_risk_manufacturers = (
            df[df["stockout_risk"]]
            .groupby("manufacturer")["inventory_level"]
            .sum()
            .sort_values(ascending=True)
        )
        high_risk_manufacturers_dict = {
            manufacturer: int(value)
            for manufacturer, value in high_risk_manufacturers.to_dict().items()
        }

        # Region-wise inventory analysis
        region_stock = df.groupby("region")["inventory_level"].sum()
        lowest_stock_regions = region_stock.nsmallest(3)
        highest_stock_regions = region_stock.nlargest(3)

        lowest_stock_regions_dict = {
            str(region): int(value)
            for region, value in lowest_stock_regions.to_dict().items()
        }
        highest_stock_regions_dict = {
            str(region): int(value)
            for region, value in highest_stock_regions.to_dict().items()
        }

        # Recommendation logic
        recommendations = []
        for low_region in lowest_stock_regions.index:
            for high_region in highest_stock_regions.index:
                recommendations.append(
                    f"Transfer stock from {high_region} to {low_region}"
                )

        return {
            "high_risk_products": high_risk_products_dict,
            "high_risk_manufacturers": high_risk_manufacturers_dict,
            "lowest_stock_regions": lowest_stock_regions_dict,
            "highest_stock_regions": highest_stock_regions_dict,
            "recommendations": recommendations
        }
