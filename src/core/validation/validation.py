class ValidationService:
    async def validate_ein(self, ein: str) -> bool:
        if not ein:
            return True
        clean_ein = ein.replace('-', '')
        return len(clean_ein) == 9 and clean_ein.isdigit()

    async def validate_duns(self, duns: str) -> bool:
        if not duns:
            return True
        clean_duns = duns.replace('-', '')
        return len(clean_duns) == 9 and clean_duns.isdigit()