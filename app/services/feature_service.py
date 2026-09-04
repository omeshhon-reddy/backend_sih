from app.schemas.risk import RiskFeatures


class FeatureService:

    @staticmethod
    def prepare(features: dict | RiskFeatures) -> dict:
        if isinstance(features, RiskFeatures):
            return features.model_dump()

        return features