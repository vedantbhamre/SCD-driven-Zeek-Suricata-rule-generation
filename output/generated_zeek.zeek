
# Auto-generated from the parsed SCD file.
# The detection logic stays the same for every testbed.
# Only the asset and GOOSE publisher data is regenerated when the
# SCD changes.

module SCDBaseline;

export {
    redef enum Notice::Type += {
        Unauthorized_Device,
        Unexpected_GOOSE_Publisher,
    };
}

# --- Data: populated from the SCD asset model ---
global known_ips: set[addr] = {
    192.168.10.11,
    192.168.10.12,
    192.168.10.21,
    192.168.10.51
};

# publisher IP -> expected APPID, keyed as a string for simplicity
global known_goose_publishers: table[addr] of string = {
    [192.168.10.11] = "1001",
    [192.168.10.12] = "1002"
};

# Detection logic: generic, does not need to change per testbed

event connection_established(c: connection)
    {
    if ( c$id$orig_h !in known_ips )
        {
        NOTICE([$note=Unauthorized_Device,
                $msg=fmt("Connection from IP not in SCD asset baseline: %s", c$id$orig_h),
                $conn=c]);
        }
    }

# TODO:
# Add GOOSE-specific event handling once the Zeek event exposed by the
# Malcolm ICS analyzer is confirmed.
#
# The asset model already contains the expected publisher -> APPID
# mapping, so this data can be used to detect unexpected APPIDs.
